import logging

import httplib2
from apiclient.discovery import build
from apiclient.errors import HttpError
from filecache import filecache
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage


PROJECT_NUMBER = ''
FLOW = flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/bigquery')


def get_most_popular_language(project_number, country='France', offset=0):
    global PROJECT_NUMBER
    PROJECT_NUMBER = project_number
    langs = get_languages_by_popularity(country)
    return langs[offset - 1]


def get_authorized_http():
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
def get_languages_by_popularity(country):
    bigquery_service = build('bigquery', 'v2', http=get_authorized_http())
    query_data = {'query': (
        "SELECT repository_language AS lang, count(repository_name) AS counts "
        "FROM [githubarchive:github.timeline] "
        "WHERE actor_attributes_location CONTAINS '{0}' "
        "AND repository_language IS NOT NULL "
        "GROUP BY lang "
        "ORDER BY counts DESC ").format(country)}
    query_request = bigquery_service.jobs()
    try:
        query_response = query_request.query(
            projectId=PROJECT_NUMBER, body=query_data).execute()
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
