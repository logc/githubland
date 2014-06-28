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

    def __init__(self, auth_user, auth_pass):
        self.auth_user = auth_user
        self.auth_pass = auth_pass

    def wait_for_rate_limit_reset(self, resource_name='search'):
        ans = requests.get(
            'https://api.github.com/rate_limit',
            auth=HTTPBasicAuth(self.auth_user, self.auth_pass))
        if any(rate['remaining'] == 0 for rate in ans['resources'].values()):
            for key, rate in ans['resources'].iteritems():
                if rate['remaining'] == 0:
                    resource_name = key
                    break
            reset = ans.json()['resources'][resource_name]['reset']
            pause = reset - time.time()
            if pause > 0:
                logging.warning("waiting for %s seconds", pause)
                time.sleep(pause)

    def get_or_wait(self, query):
        answer = requests.get(
            query, auth=HTTPBasicAuth(self.auth_user, self.auth_pass))
        if not answer.ok:
            self.wait_for_rate_limit_reset(self.auth_user, self.auth_pass)
        else:
            return answer

    def get_all_users_for_country(self, country):
        logins = []
        next_url = 'https://api.github.com/search/users?q=location:{}'.format(
            country)
        while next_url:
            answer = self.get_or_wait(next_url)
            for num_users, located_user in enumerate(answer.json()['items']):
                logins.append(located_user['login'])
            logging.warning('Users: %s in %s', num_users, country)
            if 'next' in answer.links:
                next_url = answer.links['next']['url']
            else:
                break
        return logins

    def get_language_counts_for_user(self, login):
        counts = defaultdict(lambda: 0)
        try:
            repos_query = self.get_or_wait(
                'https://api.github.com/users/{}/repos'.format(login))
            for repo in repos_query.json():
                counts[repo['language']] += 1
            return counts
        except (KeyError, ConnectionError):
            logging.exception(
                "Exception for user %s, repo %s", login, repo['name'])

    def aggregate_lang_counts_for_country(self, country):
        language_counts = defaultdict(lambda: 0)
        for user_login in self.get_all_users_for_country(country):
            for lang, count in self.get_language_counts_for_user(
                    user_login).iteritems():
                language_counts[lang] += count
        return language_counts

    def count_languages_for_countries(self, countries):
        lang_counts_by_cc = dict((c, {}) for c in countries)
        for cc in countries:
            lang_counts_by_cc[cc] = self.aggregate_lang_counts_for_country(cc)
        return lang_counts_by_cc


def main():
    passwd = getpass.getpass('Please enter your Github password: ')
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', dest='myuser')
    args = parser.parse_args()
    args.passwd = passwd
    args.func(args)


def write_out(user_logins, next_url):
    with open(RESULTSFILE, 'a') as outfile:
        outfile.write('\n'.join(user_logins))
        outfile.write('\n' + next_url + '\n')


if __name__ == '__main__':
    main()
