import datetime

import wbdata
import pandas as pd

from full_lists import full_lists


DATA_DATE = (datetime.datetime(2013, 1, 1), datetime.datetime(2014, 1, 1))
DATA_DATE2 = (datetime.datetime(2012, 1, 1), datetime.datetime(2012, 12, 31))

european_countries = [
    u'Albania', u'Andorra', u'Armenia', u'Austria', u'Azerbaijan', u'Belarus',
    u'Belgium', u'Bulgaria', u'Croatia', u'Cyprus', u'Czech Republic',
    u'Denmark', u'Estonia', u'Finland', u'France', u'Georgia', u'Germany',
    u'Greece', u'Hungary', u'Iceland', u'Ireland', u'Italy', u'Latvia',
    u'Liechtenstein', u'Lithuania', u'Luxembourg', u'Macedonia', u'Malta',
    u'Moldova', u'Monaco', u'Montenegro', u'Netherlands', u'Northern Cyprus',
    u'Norway', u'Poland', u'Portugal', u'Romania', u'Russia', u'San Marino',
    u'Serbia', u'Slovakia', u'Slovenia', u'Spain', u'Sweden', u'Switzerland',
    u'Ukraine', u'United Kingdom', u'Vatican City']
ignored = [
    'Luxembourg', 'Andorra', 'Liechtenstein', 'Macedonia', 'Malta', 'Monaco',
    'San Marino', 'Vatican City', 'Northern Cyprus']
european_countries = filter(
    lambda country: country not in ignored, european_countries)
iso_codes = {}
for country in european_countries:
    iso_code = wbdata.search_countries(country, display=False)
    if len(iso_code) == 1:
        iso_codes[country] = iso_code[0]['id']
countries = iso_codes.values()
ppps = wbdata.get_dataframe(
    {"NY.GDP.PCAP.PP.KD": "gdpppp"}, country=countries, data_date=DATA_DATE)
unemployement = wbdata.get_dataframe(
    {"SL.UEM.TOTL.ZS": "percent"}, country=countries, data_date=DATA_DATE2)
debt = wbdata.get_dataframe(
    {"GC.DOD.TOTL.GD.ZS": "debt"}, country=countries, data_date=DATA_DATE2)


def get_rankings(language):
    rankings = {}
    for k, v in full_lists.iteritems():
        try:
            rankings[k] = v.index(language)
        except ValueError:
            rankings[k] = None
    return rankings

languages = ['Haskell', 'Ruby', 'Clojure', 'Java', 'C', 'C++', 'Python',
             'JavaScript', 'Scheme', 'OCaml']
for language in languages:
    series = pd.Series(get_rankings(language))
    ppps[language] = series
    unemployement[language] = series
    debt[language] = series

unemployement = unemployement.dropna()
gdp_correlations = []
unemployment_corrs = []
debt_corrs = []
for lang in languages:
    # No need to `dropna`, since `Series.corr` drops missing values
    gdp_correlations.append(tuple([lang, ppps.gdpppp.corr(ppps[lang])]))
    unemployment_corrs.append(tuple([
        lang, unemployement.percent.corr(unemployement[lang])]))
    debt_corrs.append(tuple([
        lang, debt.debt.corr(debt[lang])]))
gdp_correlations.sort(key=lambda x: x[1])
unemployment_corrs.sort(key=lambda x: x[1], reverse=True)
debt_corrs.sort(key=lambda x: x[1], reverse=True)
print gdp_correlations
print unemployment_corrs
print debt_corrs
