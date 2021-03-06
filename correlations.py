"""
Module correlations

Produce the correlation graphs between language preference and country
macroeconomic quantities.
"""
import datetime

import wbdata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

import bigquery
from countries import get_european_country_names


DATA_DATE = (datetime.datetime(2013, 1, 1), datetime.datetime(2014, 1, 1))
DATA_DATE2 = (datetime.datetime(2012, 1, 1), datetime.datetime(2012, 12, 31))

# This line is required by matplotlib to change the default Tex font
# pylint: disable=star-args
rc('font', **{'family': 'serif', 'serif': ['Palatino']})
# pylint: enable=star-args
rc('text', usetex=True)


def get_european_countries():
    """
    Returns a list of all european countries as names, excluding some small
    countries.
    """
    ignored = [
        'Luxembourg', 'Andorra', 'Liechtenstein', 'Macedonia', 'Malta',
        'Monaco', 'San Marino', 'Vatican City', 'Northern Cyprus']
    return [country for country in get_european_country_names()
            if country not in ignored]


def get_countries_as_iso_codes():
    """
    Returns a list of countries as ISO codes
    """
    iso_codes = {}
    for country in get_european_countries():
        iso_code = wbdata.search_countries(country, display=False)
        if len(iso_code) == 1:
            iso_codes[country] = iso_code[0]['id']
    return iso_codes.values()


def get_rankings(language, project_number):
    """
    Gets the rankings of a specific language per country.  If it is the most
    preferred language, it gets number 0, if it is the second then 1, etc ...
    """
    rankings = {}
    prefs_lists = {}
    for country in get_european_countries():
        prefs_lists[country] = bigquery.get_languages_by_popularity(
            country, project_number)
    for country, languages_sorted_by_preference in prefs_lists.iteritems():
        try:
            rankings[country] = languages_sorted_by_preference.index(language)
        except ValueError:  # the language does not appear in the list
            rankings[country] = None
    return rankings


def get_economic_dataframes():
    """
    Returns dataframes for GDP at PPP, unemployment, and total government
    debt, per country
    """
    countries = get_countries_as_iso_codes()
    ppps = wbdata.get_dataframe(
        {"NY.GDP.PCAP.PP.KD": "gdpppp"}, country=countries,
        data_date=DATA_DATE)
    unemployement = wbdata.get_dataframe(
        {"SL.UEM.TOTL.ZS": "percent"}, country=countries, data_date=DATA_DATE2)
    debt = wbdata.get_dataframe(
        {"GC.DOD.TOTL.GD.ZS": "debt"}, country=countries, data_date=DATA_DATE2)
    return ppps, unemployement, debt


LANGUAGES = ['Haskell', 'Ruby', 'Clojure', 'Java', 'C', 'C++', 'Python',
             'JavaScript', 'Scheme', 'OCaml']


def add_language_rankings(dataframes, project_number):
    """ Adds a new column about language preferences to economic dataframes """
    ppps, unemployement, debt = dataframes
    for lang in LANGUAGES:
        series = pd.Series(get_rankings(lang, project_number))
        ppps[lang] = series
        unemployement[lang] = series
        debt[lang] = series
    return ppps, unemployement, debt


def correlate(project_number):
    """ Correlates economic to language preference columns in dataframes """
    dataframes = get_economic_dataframes()
    ppps, unemployement, debt = add_language_rankings(
        dataframes, project_number)
    unemployement = unemployement.dropna()
    gdp_correlations = []
    unemployment_corrs = []
    debt_corrs = []
    for lang in LANGUAGES:
        # No need to `dropna`, since `Series.corr` drops missing values
        gdp_correlations.append(tuple([lang, ppps.gdpppp.corr(ppps[lang])]))
        unemployment_corrs.append(tuple([
            lang, unemployement.percent.corr(unemployement[lang])]))
        debt_corrs.append(tuple([
            lang, debt.debt.corr(debt[lang])]))
    gdp_correlations.sort(key=lambda x: x[1])
    unemployment_corrs.sort(key=lambda x: x[1], reverse=True)
    debt_corrs.sort(key=lambda x: x[1], reverse=True)
    return gdp_correlations, unemployment_corrs, debt_corrs


def produce_figure(correlations, colorname, measure_name, filename):
    """
    Produce a bar plot figure out of the passed in correlations
    """
    def autolabel(rects, axes):
        """
        Label bars with a text right above or below the bar
        """
        for rect in rects:
            height = rect.get_y()
            vertical = 'top'
            if height == 0:
                height = rect.get_height()
                vertical = 'bottom'
            axes.text(
                rect.get_x()+rect.get_width()/2.,
                1.05*height,
                '%.2f' % height,
                ha='center', va=vertical)

    # pylint: disable=no-member
    x_values = np.arange(len(correlations))
    # pylint: enable=no-member
    width = 0.6

    _, axes = plt.subplots()
    y_values = [x[1] for x in correlations]
    rects = axes.bar(x_values, y_values, width, color=colorname, alpha=0.4)
    axes.set_ylabel(r'$\rho(%s,lang)$' % measure_name)
    axes.set_xticks(x_values+width/2.0)
    plt.ylim([1.15*min(y_values), 1.4*max(y_values)])
    langs = []
    for lang, _ in correlations:
        if lang != 'JavaScript':
            langs.append(lang)
        else:
            langs.append('JS')
    axes.set_xticklabels(tuple(langs), rotation=45)
    autolabel(rects, axes)
    plt.savefig(filename)


def produce_all_figures(project_number):
    GDP_CORRS, UNEMPLOYMENT_CORRS, DEBT_CORRS = correlate(project_number)
    produce_figure(GDP_CORRS, 'y', 'GDP', 'gdp_corr.png')
    produce_figure(UNEMPLOYMENT_CORRS, 'r', 'U', 'unemp_corr.png')
    produce_figure(DEBT_CORRS, 'b', 'D', 'debt_corr.png')
