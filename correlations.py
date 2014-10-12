import datetime

import wbdata
import pandas as pd

from full_lists import full_lists


DATA_DATE = (datetime.datetime(2013, 1, 1), datetime.datetime(2014, 1, 1))

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


def get_rankings(language):
    rankings = {}
    for k, v in full_lists.iteritems():
        try:
            rankings[k] = v.index(language)
        except ValueError:
            rankings[k] = None
    return rankings

ppps['Haskell'] = pd.Series(get_rankings('Haskell'))
ppps['Clojure'] = pd.Series(get_rankings('Clojure'))
ppps['Java'] = pd.Series(get_rankings('Java'))
ppps['C'] = pd.Series(get_rankings('C'))
ppps['C++'] = pd.Series(get_rankings('C++'))
ppps['Python'] = pd.Series(get_rankings('Python'))
ppps['JavaScript'] = pd.Series(get_rankings('JavaScript'))
ppps['Scheme'] = pd.Series(get_rankings('Scheme'))
ppps['OCaml'] = pd.Series(get_rankings('OCaml'))
langs = filter(lambda name: name != 'gdpppp', ppps.columns)
correlations = []
for lang in langs:
    # No need to `dropna`, since `Series.corr` drops missing values
    correlations.append(tuple([lang, ppps.gdpppp.corr(ppps[lang])]))
correlations.sort(key=lambda x: x[1])
print ppps
print correlations
