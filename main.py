"""
This is the main module.  You can find here the main classes to retrive
relevant infomation from Github, plus a command line interface to use them.
"""

import argparse
import getpass
import logging
import time
from collections import defaultdict

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError

RESULTSFILE = 'results.csv'


class LanguageByCountryCounts(object):
    """
    LanguageByCountryCounts is a counter table with the following
    breakdowns:

    - all countries
        - country
            - language
                - count
    Initialize the class with valid credentials and a list of countries.
    Call the class in order to perform all requests and build the internal
    table of results.
    """

    def __init__(self, auth_user, auth_pass, countries):
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.countries = countries
        self.lang_counts_by_cc = defaultdict(lambda: {})

    def __call__(self):
        for country in self.countries:
            self.lang_counts_by_cc[country] = self.__aggregate_by_country(
                country)

    def __aggregate_by_country(self, country):
        """Sums each language count for a whole country"""
        language_counts = defaultdict(lambda: 0)
        for login in self.__get_users_for_country(country):
            for lang, count in self.__get_langs_for_user(login).iteritems():
                language_counts[lang] += count
        return language_counts

    def __get_users_for_country(self, country):
        """
        Retrieves all user logins for a country from Github's search API.
        Loops over paginated results, and waits in case of hitting the rate
        limit.
        """
        logins = []
        next_url = 'https://api.github.com/search/users?q=location:{}'.format(
            country)
        while next_url:
            answer = self.__get_or_wait(next_url)
            for located_user in answer.json()['items']:
                logins.append(located_user['login'])
            if 'next' in answer.links:
                next_url = answer.links['next']['url']
            else:
                break
        return logins

    def __get_langs_for_user(self, login):
        """
        Retrieves all language counts for a user. A repository written
        (mainly) in one language counts as 1.
        """
        counts = defaultdict(lambda: 0)
        try:
            repos_query = self.__get_or_wait(
                'https://api.github.com/users/{}/repos'.format(login))
            for repo in repos_query.json():
                counts[repo['language']] += 1
            return counts
        except (KeyError, ConnectionError):
            logging.exception(
                "Exception for user %s, repo %s", login, repo['name'])

    def __wait_for_rate_limit_reset(self, resource_name='search'):
        """
        Waits the amount of time that remains until the rate limit is reset
        """
        ans = requests.get(
            'https://api.github.com/rate_limit',
            auth=HTTPBasicAuth(self.auth_user, self.auth_pass))
        if any(
                rate['remaining'] == 0 for rate in
                ans.json()['resources'].values()):
            for key, rate in ans.json()['resources'].iteritems():
                if rate['remaining'] == 0:
                    resource_name = key
                    break
            reset = ans.json()['resources'][resource_name]['reset']
            pause = reset - time.time()
            if pause > 0:
                logging.warning("waiting for %s seconds", pause)
                time.sleep(pause)

    def __get_or_wait(self, query):
        """
        Tries a query and does not fail in case the rate limit is exhausted.
        Instead, it waits until the limit is reset.
        """
        answer = requests.get(
            query, auth=HTTPBasicAuth(self.auth_user, self.auth_pass))
        if not answer.ok:
            self.__wait_for_rate_limit_reset()
        else:
            return answer


def main():
    """Parses the command line and complies with user requests"""
    passwd = getpass.getpass('Please enter your Github password: ')
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', dest='myuser')
    args = parser.parse_args()
    args.passwd = passwd
    args.func(args)


def write_out(user_logins, next_url):
    """Write out both result values and completed status to a file"""
    with open(RESULTSFILE, 'a') as outfile:
        outfile.write('\n'.join(user_logins))
        outfile.write('\n' + next_url + '\n')


if __name__ == '__main__':
    main()
