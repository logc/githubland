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

from full_lists import full_lists


DATA_DATE = (datetime.datetime(2013, 1, 1), datetime.datetime(2014, 1, 1))
DATA_DATE2 = (datetime.datetime(2012, 1, 1), datetime.datetime(2012, 12, 31))

rc('font', **{'family': 'serif', 'serif': ['Palatino']})
rc('text', usetex=True)


def get_european_countries():
    """
    Returns a list of all european countries as names, excluding some small
    countries.
    """
    european_countries = [
        u'Albania', u'Andorra', u'Armenia', u'Austria', u'Azerbaijan',
        u'Belarus', u'Belgium', u'Bulgaria', u'Croatia', u'Cyprus',
        u'Czech Republic', u'Denmark', u'Estonia', u'Finland', u'France',
        u'Georgia', u'Germany', u'Greece', u'Hungary', u'Iceland', u'Ireland',
        u'Italy', u'Latvia', u'Liechtenstein', u'Lithuania', u'Luxembourg',
        u'Macedonia', u'Malta', u'Moldova', u'Monaco', u'Montenegro',
        u'Netherlands', u'Northern Cyprus', u'Norway', u'Poland', u'Portugal',
        u'Romania', u'Russia', u'San Marino', u'Serbia', u'Slovakia',
        u'Slovenia', u'Spain', u'Sweden', u'Switzerland', u'Ukraine',
        u'United Kingdom', u'Vatican City']
    ignored = [
        'Luxembourg', 'Andorra', 'Liechtenstein', 'Macedonia', 'Malta',
        'Monaco', 'San Marino', 'Vatican City', 'Northern Cyprus']
    return [country for country in european_countries
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


def get_rankings(language):
    """
    Gets the rankings of a specific language per country.  If it is the most
    preferred language, it gets number 0, if it is the second then 1, etc ...
    """
    rankings = {}
    for country, languages_sorted_by_preference in full_lists.iteritems():
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


def add_language_rankings(dataframes):
    """ Adds a new column about language preferences to economic dataframes """
    ppps, unemployement, debt = dataframes
    for lang in LANGUAGES:
        series = pd.Series(get_rankings(lang))
        ppps[lang] = series
        unemployement[lang] = series
        debt[lang] = series
    return ppps, unemployement, debt


def correlate():
    """ Correlates economic to language preference columns in dataframes """
    dataframes = get_economic_dataframes()
    ppps, unemployement, debt = add_language_rankings(dataframes)
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
    def autolabel(rects, ax):
        for rect in rects:
            height = rect.get_y()
            vertical = 'top'
            if height == 0:
                height = rect.get_height()
                vertical = 'bottom'
            ax.text(
                rect.get_x()+rect.get_width()/2.,
                1.05*height,
                '%.2f' % height,
                ha='center', va=vertical)

    N = len(correlations)
    xs = np.arange(N)
    width = 0.6

    fig, ax = plt.subplots()
    ys = [x[1] for x in correlations]
    rects = ax.bar(xs, ys, width, color=colorname, alpha=0.4)
    ax.set_ylabel(r'$\rho(%s,lang)$' % measure_name)
    ax.set_xticks(xs+width/2.0)
    plt.ylim([1.15*min(ys), 1.4*max(ys)])
    langs = []
    for lang, corr in correlations:
        if lang != 'JavaScript':
            langs.append(lang)
        else:
            langs.append('JS')
    ax.set_xticklabels(tuple(langs), rotation=45)
    autolabel(rects, ax)
    plt.savefig(filename)


if __name__ == '__main__':
    GDP_CORRS, UNEMPLOYMENT_CORRS, DEBT_CORRS = correlate()
    produce_figure(GDP_CORRS, 'y', 'GDP', 'gdp_corr.png')
    produce_figure(UNEMPLOYMENT_CORRS, 'r', 'U', 'unemp_corr.png')
    produce_figure(DEBT_CORRS, 'b', 'D', 'debt_corr.png')
