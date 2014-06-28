import json

import responses
from nose.tools import assert_equals

import main


class TestLanguageByCountryCounts(object):
    user, password = 'fake', 'fake'
    instance = main.LanguageByCountryCounts(user, password)
    cc = "Spain"
    fst_user_login = "mojombo"
    snd_user_login = "logc"
    base = 'https://api.github.com/search/users'
    fst_user_query = '{0}?q=location:{1}'.format(base, cc)
    snd_user_query = '{0}?q=location%3A{1}&page=2'.format(base, cc)
    fst_user_response = {
        "total_count": 2,
        "incomplete_results": False,
        "items": [{
            "login": fst_user_login,
            "id": 1,
            # ... other infos skipped ...
            "score": 105.47857}]}
    snd_user_response = {
        "total_count": 2,
        "incomplete_results": False,
        "items": [{
            "login": snd_user_login,
            "id": 2,
            # ... other infos skipped ...
            "score": 10.357}]}
    fst_user_links = {
        'Link': '<{0}?q=location%3A{1}&page=2>; rel="next",'.format(base, cc) +
                '<{0}?q=location%3A{1}&page=2>; rel="last"'.format(base, cc)}
    snd_user_links = {
        'Link':
            '<{0}?q=location%3A{1}&page=2>; rel="last",'.format(base, cc) +
            '<{0}?q=location%3A{1}&page=1>; rel="first",'.format(base, cc) +
            '<{0}?q=location%3A{1}&page=1>; rel="prev"'.format(base, cc)}
    fst_repos_query = 'https://api.github.com/users/{}/repos'.format(
        fst_user_login)
    snd_repos_query = 'https://api.github.com/users/{}/repos'.format(
        snd_user_login)
    fst_repos_response = [{
        "id": 1296268,
        "owner": {
            "login": fst_user_login,
            "id": 1,
            # ... other infos skipped ...
            },
        "name": "Hello-World",
        "full_name": "{}/Hello-World".format(fst_user_login),
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
            "login": fst_user_login,
            "id": 1,
            # ... other infos skipped ...
            },
        "name": "Hello-Man",
        "full_name": "{}/Hello-Man".format(fst_user_login),
        # ... other infos skipped ...
        "language": "Java",
        "forks_count": 9,
        "stargazers_count": 80,
        "watchers_count": 80,
        # ... other infos skipped ...
        }
        ]
    snd_repos_response = [{
        "id": 1296270,
        "owner": {
            "login": snd_user_login,
            "id": 2,
            # ... other infos skipped ...
            },
        "name": "Hello-World",
        "full_name": "{}/Hello-World".format(snd_user_login),
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
            "login": snd_user_login,
            "id": 2,
            # ... other infos skipped ...
            },
        "name": "Bye-World",
        "full_name": "{}/Bye-World".format(snd_user_login),
        # ... other infos skipped ...
        "language": "Java",
        "forks_count": 9,
        "stargazers_count": 80,
        "watchers_count": 80,
        # ... other infos skipped ...
        }]

    def add_response(self, to_query, response, links=None):
        responses.add(
            responses.GET, to_query, match_querystring=True,
            body=json.dumps(response),
            adding_headers=links,
            status=200, content_type='application/json')

    def setup(self):
        self.add_response(
            self.fst_user_query, self.fst_user_response, self.fst_user_links)
        self.add_response(
            self.snd_user_query, self.snd_user_response, self.snd_user_links)
        self.add_response(self.fst_repos_query, self.fst_repos_response)
        self.add_response(self.snd_repos_query, self.snd_repos_response)

    @responses.activate
    def test_get_all_users_for_country(self):
        user_logins = self.instance.get_all_users_for_country(self.cc)
        assert_equals(user_logins, [self.fst_user_login, self.snd_user_login])

    @responses.activate
    def test_get_language_counts_for_user(self):
        fst_user_langs = self.instance.get_language_counts_for_user(
            self.fst_user_login)
        snd_user_langs = self.instance.get_language_counts_for_user(
            self.snd_user_login)
        assert_equals(fst_user_langs, {'Java': 2})
        assert_equals(snd_user_langs, {'Python': 1, 'Java': 1})

    @responses.activate
    def test_aggregate_lang_counts_for_country(self):
        language_counts = self.instance.aggregate_lang_counts_for_country(
            self.cc)
        expected = {'Java': 3, 'Python': 1}
        assert_equals(language_counts, expected)

    @responses.activate
    def test_count_languages_for_countries(self):
        fr_cc = "France"
        fr_user_login = "olala"
        fr_user_query = '{0}?q=location:{1}'.format(self.base, fr_cc)
        fr_user_response = {
            "total_count": 1,
            "incomplete_results": False,
            "items": [{
                "login": fr_user_login,
                "id": 100,
                # ... other infos skipped ...
                "score": 105.47857}]}
        fr_repos_query = 'https://api.github.com/users/{}/repos'.format(
            fr_user_login)
        fr_repos_response = [{
            "id": 1296268,
            "owner": {
                "login": fr_user_login,
                "id": 100,
                # ... other infos skipped ...
                },
            "name": "Bonjour-World",
            "full_name": "{}/Bonjour-World".format(fr_user_login),
            # ... other infos skipped ...
            "language": "OCaml",
            "forks_count": 9,
            "stargazers_count": 80,
            "watchers_count": 80,
            # ... other infos skipped ...
            }]
        self.add_response(fr_user_query, fr_user_response)
        self.add_response(fr_repos_query, fr_repos_response)
        language_counts_by_cc = self.instance.count_languages_for_countries(
            [self.cc, fr_cc])
        expected = {
            'Spain': {'Java': 3, 'Python': 1},
            'France': {'OCaml': 1}}
        assert_equals(language_counts_by_cc, expected)
