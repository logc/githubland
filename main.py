import argparse
import getpass
import logging
import os
import os.path
import sys
import time
import urlparse
from collections import defaultdict

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError

RESULTSFILE = 'results.csv'


def add_followers(root, user, password, user_graph, visited,
                  recursion_depth=2):
    if recursion_depth == 0:
        return user_graph
    user_graph.add_node(root)
    visited.add(root)
    answer = get_or_wait(
        user, password,
        'https://api.github.com/users/{0}/followers'.format(root))
    followers = answer.json()
    for follower in followers:
        follower = follower['login']
        user_graph.add_edge(root, follower)
        if follower not in visited:
            add_followers(
                follower, user, password, user_graph, visited,
                recursion_depth - 1)
    return user_graph


def read_and_maybe_delete_last_line(filehandle):
    filehandle.seek(0, os.SEEK_END)
    pos = filehandle.tell() - 1
    while pos > 0 and filehandle.read(1) != "\n":
        pos -= 1
        filehandle.seek(pos, os.SEEK_SET)
    filehandle.seek(pos, os.SEEK_SET)
    last_line = filehandle.readlines()[-1]
    if last_line.startswith('https://api.github.com/users?'):
        filehandle.seek(pos, os.SEEK_SET)
        filehandle.truncate()
        return last_line.strip()


def determine_starting_url():
    next_url = 'https://api.github.com/users'
    if os.path.isfile(RESULTSFILE):
        with open(RESULTSFILE, 'r+') as resultsfile:
            relevant_last_line = read_and_maybe_delete_last_line(resultsfile)
            if relevant_last_line:
                next_url = relevant_last_line
    return next_url


def get_last_page_number(response):
    parsed = urlparse.urlparse(response.links['last']['url'])
    params = urlparse.parse_qs(parsed.query)
    assert len(params['page']) == 1
    return int(params['page'][0])


def get_all_users(args):
    next_url = determine_starting_url()
    user_logins = []
    request_count = 0
    try:
        while next_url:
            request_count += 1
            sys.stdout.write(
                "\rDoing request {}, {} users found so far".format(
                    request_count, len(user_logins)))
            sys.stdout.flush()
            try:
                answer = get_or_wait(args.myuser, args.password, next_url)
                next_url = answer.links['next']['url']
            except ConnectionError:
                logging.exception("Conection error for url %s", next_url)
                continue
            for user in answer.json()['items']:
                user_logins.append(user['login'])
    except KeyboardInterrupt:
        write_out(user_logins, next_url)
    finally:
        write_out(user_logins, next_url)


def get_users_per_country(args):
    search_users_per_country(args.myuser, args.passwd)


def wait_for_rate_limit_reset(user, password, resource_name='search'):
    answer = requests.get(
        'https://api.github.com/rate_limit',
        auth=HTTPBasicAuth(user, password))
    if any(rate['remaining'] == 0 for rate in answer['resources'].values()):
        for key, rate in answer['resources'].iteritems():
            if rate['remaining'] == 0:
                resource_name = key
                break
        reset = answer.json()['resources'][resource_name]['reset']
        pause = reset - time.time()
        if pause > 0:
            logging.warning("waiting for %s seconds", pause)
            time.sleep(pause)


def get_or_wait(user, password, query):
    answer = requests.get(query, auth=HTTPBasicAuth(user, password))
    if not answer.ok:
        wait_for_rate_limit_reset(user, password)
    else:
        return answer


def get_repos_for_user(user, password, login):
    counts = defaultdict(lambda: 0)
    try:
        repos_query = get_or_wait(
            user, password,
            'https://api.github.com/users/{}/repos'.format(login))
        for repo in repos_query.json():
            counts[repo['language']] += 1
        return counts
    except (KeyError, ConnectionError):
        logging.exception(
            "Exception for user %s, repo %s", login, repo['name'])


def get_all_users_for_country(user, password, country):
    logins = []
    next_url = 'https://api.github.com/search/users?q=location:{}'.format(
        country)
    while next_url:
        answer = get_or_wait(user, password, next_url)
        for num_users, located_user in enumerate(answer.json()['items']):
            logins.append(located_user['login'])
        logging.warning('Users: %s in %s', num_users, country)
        if 'next' in answer.links:
            next_url = answer.links['next']['url']
        else:
            break
    return logins


def search_users_per_country(user, password):
    countries = ['Spain', 'Germany', 'France', 'Italy', 'UK']
    try:
        for country in countries:
            count_languages(user, password, country)
    finally:
        print total_countries_counts
        print countries_counts
        if counts:
            print counts


def count_languages(user, password, country):
    total_countries_counts = dict((c, 0) for c in countries)
    countries_counts = dict((c, None) for c in countries)
    counts = None
    try:
        logging.warning('Starting %s', country)
        user_logins = get_all_users_for_country(user, password, country)
        for user_login in user_logins:
            counts = get_repos_for_user(
                user, password, user_login)
        countries_counts[country] = counts
        return countries_counts


def main():
    passwd = getpass.getpass('Please enter your Github password: ')
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', dest='myuser')
    subparsers = parser.add_subparsers()
    parser_all_users = subparsers.add_parser('all_users')
    parser_all_users.set_defaults(func=get_all_users)
    parser_users_per_country = subparsers.add_parser('users_per_country')
    parser_users_per_country.set_defaults(func=get_users_per_country)
    args = parser.parse_args()
    args.passwd = passwd
    args.func(args)


def write_out(user_logins, next_url):
    with open(RESULTSFILE, 'a') as outfile:
        outfile.write('\n'.join(user_logins))
        outfile.write('\n' + next_url + '\n')


if __name__ == '__main__':
    main()
