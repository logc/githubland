"""
As read in:
http://jcastellssala.wordpress.com/2012/06/19/europe-countries-dbpediasparqlpython/
"""
import logging
import posixpath
import re
from urlparse import urlparse

from filecache import filecache
from SPARQLWrapper import SPARQLWrapper, JSON


@filecache(30 * 24 * 3600)
def get_european_country_names():
    """Get European country names from a remote service that knows about such
    entities as countries and Europe."""
    logging.debug("Querying DBpedia about Europe")
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery("""
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX dbprop: <http://dbpedia.org/property/>
    PREFIX yago: <http://dbpedia.org/class/yago/>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

    SELECT DISTINCT ?place WHERE {
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
        name = path_parts[-1]
        name = re.sub(r"_", " ", name)
        name = re.sub(r"Republic of ", "", name)
        name = re.sub(r" \(country\)", "", name)
        names.append(name)
    logging.warning("Found the following countries: {}".format(sorted(names)))
    return sorted(names)
