import getpass
import sys

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError


def add_followers(root, user, password, user_graph, visited,
                  recursion_depth=2):
    if recursion_depth == 0:
        return user_graph
    user_graph.add_node(root)
    visited.add(root)
    answer = requests.get(
        'https://api.github.com/users/{0}/followers'.format(root),
        auth=HTTPBasicAuth(user, password))
    followers = answer.json()
    for follower in followers:
        follower = follower['login']
        user_graph.add_edge(root, follower)
        if follower not in visited:
            add_followers(
                follower, user, password, user_graph, visited,
                recursion_depth - 1)
    return user_graph


def main():
    username = sys.argv[1]
    password = getpass.getpass('Please enter your Github password: ')
    user_logins = []
    request_count = 0
    next_url = 'https://api.github.com/users'
    try:
        while next_url:
            request_count += 1
            sys.stdout.write(
                "\rDoing request {}, {} users found so far".format(
                    request_count, len(user_logins)))
            sys.stdout.flush()
            answer = requests.get(
                next_url,
                auth=HTTPBasicAuth(username, password))
            users = answer.json()
            for user in users:
                user_logins.append(user['login'])
            next_url = answer.links['next']['url']
    except KeyboardInterrupt:
        write_out(user_logins, next_url)
    finally:
        write_out(user_logins, next_url)


def write_out(user_logins, next_url):
    with open('results.csv', 'a') as outfile:
        outfile.write('\n'.join(user_logins))
        outfile.write('\n' + next_url)


if __name__ == '__main__':
    main()
