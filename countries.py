"""
As read in:
http://jcastellssala.wordpress.com/2012/06/19/europe-countries-dbpediasparqlpython/
"""
import posixpath
import re
from urlparse import urlparse

from SPARQLWrapper import SPARQLWrapper, JSON


sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

sparql.setQuery("""
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

SELECT ?place WHERE {
    ?place dcterms:subject category:Member_states_of_the_European_Union.
    ?place a yago:EuropeanCountries.
    ?place a dbpedia-owl:Country.
}
""")

results = sparql.query().convert()
names = []
for result in results['results']['bindings']:
    path = urlparse(result['place']['value']).path
    path_parts = posixpath.split(path)
    assert len(path_parts) == 2, "result path malformed"
    name_candidate = path_parts[-1]
    name = re.sub("_", " ", name_candidate)
    names.append(name)

for name in sorted(names):
    print name
