import logging

import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage


PROJECT_NUMBER = '413790172023'
FLOW = flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/bigquery')


def get_most_popular_language(country='France', offset=0):
    # TODO: split into authorization and retrieval functions
    storage = Storage('bigquery_credentials.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        from oauth2client import tools
        # Run oauth2 flow with default arguments.
        credentials = tools.run_flow(
            FLOW, storage, tools.argparser.parse_args([]))
    http = httplib2.Http()
    http = credentials.authorize(http)
    # TODO: cache results into a shelve file
    bigquery_service = build('bigquery', 'v2', http=http)
    query_data = {'query': (
        "SELECT repository_language AS lang, count(repository_name) AS counts "
        "FROM [githubarchive:github.timeline] "
        "WHERE actor_attributes_location CONTAINS '{0}' "
        "AND repository_language IS NOT NULL "
        "GROUP BY lang "
        "ORDER BY counts DESC ").format(country)}
    query_request = bigquery_service.jobs()
    query_response = query_request.query(
        projectId=PROJECT_NUMBER, body=query_data).execute()
    try:
        first_row = query_response['rows'][offset]
        language = first_row['f'][0]['v']
    except KeyError:
        logging.exception(query_response.keys())
        language = 'No data'
    return language
