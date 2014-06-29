"""These are the main tests for githubland"""
import json

import responses
# pylint: disable=no-name-in-module
from nose.tools import assert_equals
# pylint: enable=no-name-in-module

import main


class TestLanguageByCountryCounts(object):
    """Tests for the class LanguageByCountryCounts"""

    def __init__(self):
        self.instance = main.LanguageByCountryCounts(USER, PWD, [CC, FR_CC])

    def setup(self):
        """Setup test fixture"""
        self.add_response(FST_USER_QUERY, FST_USER_RESPONSE, FST_USER_LINKS)
        self.add_response(SND_USER_QUERY, SND_USER_RESPONSE, SND_USER_LINKS)
        self.add_response(FST_REPOS_QUERY, FST_REPOS_RESPONSE)
        self.add_response(SND_REPOS_QUERY, SND_REPOS_RESPONSE)
        self.add_response(FR_USER_QUERY, FR_USER_RESPONSE)
        self.add_response(FR_REPOS_QUERY, FR_REPOS_RESPONSE)

    @staticmethod
    def add_response(to_query, response, links=None):
        """Helper method to setup.  Adds a response to the mock API"""
        responses.add(
            responses.GET, to_query, match_querystring=True,
            body=json.dumps(response),
            adding_headers=links,
            status=200, content_type='application/json')

    @responses.activate
    def test_count_languages(self):
        """Checks that for two different countries, with two users in one and
        one user in the other, who have one common language and two other
        languages not in common, the resulting values are correct"""
        self.instance()
        expected = {
            'Spain': {'Java': 3, 'Python': 1},
            'France': {'OCaml': 1}}
        assert_equals(self.instance.lang_counts_by_cc, expected)

USER, PWD = "fake", "fake"
CC = "Spain"
FST_USER_LOGIN = "mojombo"
SND_USER_LOGIN = "logc"
BASE = 'https://api.github.com/search/users'
FST_USER_QUERY = '{0}?q=location:{1}'.format(BASE, CC)
SND_USER_QUERY = '{0}?q=location%3A{1}&page=2'.format(BASE, CC)
FST_USER_RESPONSE = {
    "total_count": 2,
    "incomplete_results": False,
    "items": [{
        "login": FST_USER_LOGIN,
        "id": 1,
        # ... other infos skipped ...
        "score": 105.47857}]}
SND_USER_RESPONSE = {
    "total_count": 2,
    "incomplete_results": False,
    "items": [{
        "login": SND_USER_LOGIN,
        "id": 2,
        # ... other infos skipped ...
        "score": 10.357}]}
FST_USER_LINKS = {
    'Link': '<{0}?q=location%3A{1}&page=2>; rel="next",'.format(BASE, CC) +
            '<{0}?q=location%3A{1}&page=2>; rel="last"'.format(BASE, CC)}
SND_USER_LINKS = {
    'Link':
        '<{0}?q=location%3A{1}&page=2>; rel="last",'.format(BASE, CC) +
        '<{0}?q=location%3A{1}&page=1>; rel="first",'.format(BASE, CC) +
        '<{0}?q=location%3A{1}&page=1>; rel="prev"'.format(BASE, CC)}
FST_REPOS_QUERY = 'https://api.github.com/users/{}/repos'.format(
    FST_USER_LOGIN)
SND_REPOS_QUERY = 'https://api.github.com/users/{}/repos'.format(
    SND_USER_LOGIN)
FST_REPOS_RESPONSE = [{
    "id": 1296268,
    "owner": {
        "login": FST_USER_LOGIN,
        "id": 1,
        # ... other infos skipped ...
        },
    "name": "Hello-World",
    "full_name": "{}/Hello-World".format(FST_USER_LOGIN),
    # ... other infos skipped ...
    "language": "Java",
    "forks_count": 9,
    "stargazers_count": 80,
    "watchers_count": 80,
    # ... other infos skipped ...
    },
    {
    "id": 1296269,
    "owner": {
        "login": FST_USER_LOGIN,
        "id": 1,
        # ... other infos skipped ...
        },
    "name": "Hello-Man",
    "full_name": "{}/Hello-Man".format(FST_USER_LOGIN),
    # ... other infos skipped ...
    "language": "Java",
    "forks_count": 9,
    "stargazers_count": 80,
    "watchers_count": 80,
    # ... other infos skipped ...
    }
    ]
SND_REPOS_RESPONSE = [{
    "id": 1296270,
    "owner": {
        "login": SND_USER_LOGIN,
        "id": 2,
        # ... other infos skipped ...
        },
    "name": "Hello-World",
    "full_name": "{}/Hello-World".format(SND_USER_LOGIN),
    # ... other infos skipped ...
    "language": "Python",
    "forks_count": 9,
    "stargazers_count": 80,
    "watchers_count": 80,
    # ... other infos skipped ...
    },
    {
    "id": 1296271,
    "owner": {
        "login": SND_USER_LOGIN,
        "id": 2,
        # ... other infos skipped ...
        },
    "name": "Bye-World",
    "full_name": "{}/Bye-World".format(SND_USER_LOGIN),
    # ... other infos skipped ...
    "language": "Java",
    "forks_count": 9,
    "stargazers_count": 80,
    "watchers_count": 80,
    # ... other infos skipped ...
    }]
FR_CC = "France"
FR_USER_LOGIN = "olala"
FR_USER_QUERY = '{0}?q=location:{1}'.format(BASE, FR_CC)
FR_USER_RESPONSE = {
    "total_count": 1,
    "incomplete_results": False,
    "items": [{
        "login": FR_USER_LOGIN,
        "id": 100,
        # ... other infos skipped ...
        "score": 105.47857}]}
FR_REPOS_QUERY = 'https://api.github.com/users/{}/repos'.format(
    FR_USER_LOGIN)
FR_REPOS_RESPONSE = [{
    "id": 1296268,
    "owner": {
        "login": FR_USER_LOGIN,
        "id": 100,
        # ... other infos skipped ...
        },
    "name": "Bonjour-World",
    "full_name": "{}/Bonjour-World".format(FR_USER_LOGIN),
    # ... other infos skipped ...
    "language": "OCaml",
    "forks_count": 9,
    "stargazers_count": 80,
    "watchers_count": 80,
    # ... other infos skipped ...
    }]
