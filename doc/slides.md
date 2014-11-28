% Githubland
% Luis Osa \scriptsize\<luis.osa.gdc@gmail.com\>
% November 2014

# Motivation: No code rule

- "Data beers" rules do not allow to show code during talks.

- But **data is the same as code**! 

    (cf. [Lisp
    homoiconicity](http://en.wikipedia.org/wiki/Homoiconicity#Homoiconicity_in_Lisp),
    [Unix "rule of
    representation"](http://en.wikipedia.org/wiki/Unix_philosophy))

# Where is there a lot of code? Github

$\vcenter{\hbox{\includegraphics[width=.15\textwidth, height=.5\textheight]{img/Git-logo.pdf}}}$
is the VCS developed by the Linux kernel team

$\vcenter{\hbox{\includegraphics[width=.1\textwidth, height=.5\textheight]{img/octocat.png}}}$
$\vcenter{\hbox{\includegraphics[width=.15\textwidth, height=.5\textheight]{img/GitHub_logo_2013.pdf}}}$
is a Git repository web-based hosting service

# Inspiration: Blatt maps

- U.S. Census Bureau data on second languages in American households [^3]

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

# Processing Github information

- Github offers a REST API, but it has rate limits
- [GitHub Archive](http://www.githubarchive.org) publishes all public commits
  in hourly archives
- [Google BigQuery](https://cloud.google.com/bigquery/) has the Github timeline
  as public data

\centering{\includegraphics[width=.5\textwidth, height=.4\textheight]{img/bigquery-logo.png}}

# Which countries are there in Europe?

- There may be new countries:
$\vcenter{\hbox{\includegraphics[width=.25\textwidth, height=.78\textheight]{img/new_countries.png}}}$

- There may be less countries:
$\vcenter{\hbox{\includegraphics[width=.125\textwidth, height=.78\textheight]{img/ukraine.png}}}$

- A solution: DBpedia and SPARQL

DBpedia has a [SPARQL endpoint](http://dbpedia.org/sparql) to **receive
queries**. There are [wrapper
libraries](https://pypi.python.org/pypi/SPARQLWrapper) 

# No Twitter

\centering{\includegraphics[width=.5\textwidth, height=.4\textheight]{img/no_twitter.jpg}}

- Quite tired of people categorizing tweets.  There are many APIs out there!
- Do not worry, we are still going to get rich! $\rightarrow$ using World Bank macroeconomic data [^sherouse]

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

# Take away messages

- Data talk about code!

. . . 

- SPARQL and other APIs: all data is on your laptop

. . . 

- BigQuery and other tools: your laptop controls clusters

. . . 

- **All languages are beautiful**

. . . 

- but do not program in OCaml if you can avoid it
