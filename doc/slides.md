% Githubland
% Luis Osa \scriptsize\<luis.osa.gdc@gmail.com\>
% October 2014

# Inspiration: No code rule

"Data beers" rules do not allow to show code.  But data is the same as code!

- [homoiconicity in Lisp](http://en.wikipedia.org/wiki/Homoiconicity#Homoiconicity_in_Lisp): Lisp statements are the same as Lisp lists!

- [Unix philosophy](http://en.wikipedia.org/wiki/Unix_philosophy), "Rule of Representation": fold logic into data to have robust programs

# Where is there a lot of code? Github

$\vcenter{\hbox{\includegraphics[width=.15\textwidth, height=.5\textheight]{img/Git-logo.pdf}}}$
is the VCS developed by the Linux kernel team

$\vcenter{\hbox{\includegraphics[width=.1\textwidth, height=.5\textheight]{img/octocat.png}}}$
$\vcenter{\hbox{\includegraphics[width=.15\textwidth, height=.5\textheight]{img/GitHub_logo_2013.pdf}}}$
is a Git repository web-based hosting service

> As of 2014, Github reports having over 3.4 million users [^1], making it the largest code host in the world. [^2]

[^1]: [Whitaker, Marisa](http://magazine.uc.edu/favorites/web-only/wanstrath.html) (April 2014).
[^2]: Georgios Gousios; et al.. [Lean GHTorrent: GitHub Data on Demand](http://flosshub.org/sites/flosshub.org/files/lean-ghtorrent.pdf) (2014)

# Inspiration: Blatt maps

- Take data on second languages from the U.S. Census Bureau
- Remove the most popular second language, Spanish, to uncover a much more diverse map [^3]

\includegraphics[width=.5\textwidth]{img/usa1.png} \ \ 
\includegraphics[width=.5\textwidth]{img/usa2.png}

[^3]: http://gizmodo.com/the-most-common-languages-spoken-in-the-u-s-state-by-1575719698

# European (programming) languages

![Most popular languages](img/languages.png)

# European (programming) languages

![The problem is Octopress](img/languages_and_octopress.png)

# European (programming) languages

![Most popular languages excluding JavaScript](img/languages_excluding_JS.png)

# European (programming) languages

![The problem is the web](img/languages_and_web.png)

# European (programming) languages

![Most popular languages excluding JavaScript and PHP](img/languages_excluding_JS_PHP.png)

# Which countries are there in Europe?

- Writing a static list is tedious and error-prone:

    - there may be new countries:
$\vcenter{\hbox{\includegraphics[width=.25\textwidth, height=.78\textheight]{img/new_countries.png}}}$

    - there may be less countries:
$\vcenter{\hbox{\includegraphics[width=.125\textwidth, height=.78\textheight]{img/ukraine.png}}}$

# Which countries are there in Europe? (cont.)

- the solution: DBpedia and SPARQL
    - DBpedia: extracts structured content from Wikipedia
    - SPARQL: RDF query language

DBpedia has a SPARQL endpoint[^endpoint] to **receive queries**

[^endpoint]: http://dbpedia.org/sparql

# Which countries are there in Europe? (cont.)

```sql
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>

SELECT DISTINCT ?place WHERE {
    ?place a yago:EuropeanCountries.
    ?place a dbpedia-owl:Country.
}
```

You can issue this query from a program using a wrapper library [^4]. Used to
get the countries in the previous maps [^filter]


[^4]: https://pypi.python.org/pypi/SPARQLWrapper
[^filter]: filtering out: ['Luxembourg', 'Andorra', 'Liechtenstein', 'Macedonia',
  'Malta', 'Monaco', 'San Marino', 'Vatican City', 'Northern Cyprus']

# Processing Github information

- Github offers a REST API, but it has rate limits
- [GitHub Archive](http://www.githubarchive.org): public GitHub
  timeline in aggregated hourly archives, i.e. `
  http://data.githubarchive.org/2012-04-11-15.json.gz`
- [Google BigQuery](https://cloud.google.com/bigquery/) has the Github timeline
  as public data

# No Twitter

![Twitter considered harmful](img/no_twitter.png)

- Quite tired of people categorizing tweets.  There are many APIs out there!
- Do not worry, we are still going to join our results so far to economic data and get rich!

# World Bank data

\centering\includegraphics[height=.4\textheight]{img/world-bank-logo.jpg}

- World Bank development and macroeconomic data are available [online](http://data.worldbank.org)
- `wbdata` is a library to access them from a Python script [^sherouse] 

[^sherouse]: Sherouse, Oliver (2014). Wbdata. Arlington, VA. Available from http://github.com/OliverSherouse/wbdata.

# Google Correlations

!["Clojure programming destroys jobs", Del Cacho, Carlos, 2014](img/screenshot.png)

# $corr(GDP, language)$

![Pearson correlation of GDP with language preference [^negative]](img/gdp_corr.png)

[^negative]: Negative values denote a language used in richer countries; a
low value in the language precedence means a higher place in the language
preference list for a country.

# $corr(unemployment, language)$

![Pearson correlation of unemployment with language preference[^positive]](img/unemp_corr.png)

[^positive]: Positive values show preferred languages in countries with low unemployment

# $corr(debt, language)$

![Pearson correlation of total government debt as % of GDP with language preference[^positive2]](img/debt_corr.png)

[^positive2]: Positive values show preferred languages in countries with low debt

# Choose your country

![European languages excluding JS and PHP](img/languages_excluding_JS_PHP.png)

# Take away messages

- Data talk about code!

. . . 

- SPARQL and other APIs: all data is on your laptop

. . . 

- BigQuery and other tools: your laptop controls clusters

. . . 

- **All languages are beautiful**

. . . 

- but do not code in OCaml if you care about your country!
