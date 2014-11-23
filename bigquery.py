"""
Module bigquery

Query the Google BigQuery service about Github public timeline.
Also, create the necessary credentials if not already created.
"""
import logging

import httplib2
from apiclient.discovery import build
from apiclient.errors import HttpError
from filecache import filecache
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage


FLOW = flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/bigquery')


def get_most_popular_language(project_number, country='France', offset=0):
    """Returns the most popular language for a country, with an offset, i.e. if
    offset is 1, then the second most popular language is returned."""
    langs = get_languages_by_popularity(country, project_number)
    return langs[offset - 1]


def get_authorized_http():
    """Returns an authorized Http instance, for use in queries to the
    service"""
    storage = Storage('bigquery_credentials.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        from oauth2client import tools
        # Run oauth2 flow with default arguments.
        credentials = tools.run_flow(
            FLOW, storage, tools.argparser.parse_args([]))
    http = httplib2.Http()
    http = credentials.authorize(http)
    return http


@filecache(2 * 30 * 24 * 3600)
def get_languages_by_popularity(country, project_number):
    """Queries the service about language popularity for a specific country,
    returning all aggregated commit counts grouped by language, in
    descending order of count."""
    bigquery_service = build('bigquery', 'v2', http=get_authorized_http())
    query_data = {'query': (
        "SELECT repository_language AS lang, count(repository_name) AS counts "
        "FROM [githubarchive:github.timeline] "
        "WHERE actor_attributes_location CONTAINS '{0}' "
        "AND repository_language IS NOT NULL "
        "GROUP BY lang "
        "ORDER BY counts DESC ").format(country)}
    # The Resource instance gets the `jobs` member at runtime
    # pylint: disable=no-member
    query_request = bigquery_service.jobs()
    try:
        query_response = query_request.query(
            projectId=project_number, body=query_data).execute()
    except HttpError as err:
        raise RuntimeError(err)
    languages = []
    for row in query_response['rows']:
        try:
            languages.append(row['f'][0]['v'])
        except KeyError:
            logging.exception(query_response.keys())
            languages.append('No data')
    return languages
