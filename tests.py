import json

import responses
from nose.tools import assert_equals, with_setup

import main

USER_LOGIN = "mojombo"
ANOTHER_USER_LOGIN = "logc"
COUNTRY = "Spain"


def setup():
    cc = COUNTRY
    base = 'https://api.github.com/search/users'
    user_query = '{0}?q=location:{1}'.format(base, cc)
    users_response = {
        "total_count": 2,
        "incomplete_results": False,
        "items": [{
            "login": USER_LOGIN,
            "id": 1,
            "avatar_url": "whatever",
            "gravatar_id": "25c7c18223fb42a4c6ae1c8db6f50f9b",
            "url": "https://api.github.com/users/mojombo",
            "html_url": "https://github.com/mojombo",
            "followers_url": "whatever",
            "subscriptions_url": "whatever",
            "organizations_url": "https://api.github.com/users/mojombo/orgs",
            "repos_url": "https://api.github.com/users/mojombo/repos",
            "received_events_url": "whatever",
            "type": "User",
            "score": 105.47857}]}
    user_links = {
        'Link': '<{0}?q=location%3A{1}&page=2>; rel="next",'.format(base, cc) +
                '<{0}?q=location%3A{1}&page=2>; rel="last"'.format(base, cc)}
    user_last_query = '{0}?q=location%3A{1}&page=2'.format(base, cc)
    user_last_response = {
        "total_count": 2,
        "incomplete_results": False,
        "items": [{
            "login": ANOTHER_USER_LOGIN,
            "id": 2,
            "avatar_url": "whatever",
            "gravatar_id": "25c7c18223fb42a4c6ae1c8db6f50f9b",
            "url": "https://api.github.com/users/logc",
            "html_url": "https://github.com/logc",
            "followers_url": "whatever",
            "subscriptions_url": "whatever",
            "organizations_url": "https://api.github.com/users/logc/orgs",
            "repos_url": "https://api.github.com/users/logc/repos",
            "received_events_url": "whatever",
            "type": "User",
            "score": 10.357}]}
    user_last_links = {
        'Link':
            '<{0}?q=location%3A{1}&page=2>; rel="last",'.format(base, cc) +
            '<{0}?q=location%3A{1}&page=1>; rel="first",'.format(base, cc) +
            '<{0}?q=location%3A{1}&page=1>; rel="prev"'.format(base, cc)}
    repos_query = 'https://api.github.com/users/{}/repos'.format(USER_LOGIN)
    repos_response = [{
        "id": 1296269,
        "owner": {
            "login": USER_LOGIN,
            "id": 1,
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "gravatar_id": "somehexcode",
            "url": "https://api.github.com/users/octocat",
            "html_url": "https://github.com/octocat",
            "followers_url": "https://api.github.com/users/octocat/followers",
            "following_url": "whatever",
            "gists_url": "whatever",
            "starred_url": "whatever",
            "subscriptions_url": "whatever",
            "organizations_url": "https://api.github.com/users/octocat/orgs",
            "repos_url": "https://api.github.com/users/octocat/repos",
            "events_url": "whatever",
            "received_events_url": "whatever",
            "type": "User",
            "site_admin": False
            },
        "name": "Hello-World",
        "full_name": "octocat/Hello-World",
        "description": "This your first repo!",
        "private": False,
        "fork": False,
        "url": "https://api.github.com/repos/octocat/Hello-World",
        "html_url": "https://github.com/octocat/Hello-World",
        "clone_url": "https://github.com/octocat/Hello-World.git",
        "git_url": "git://github.com/octocat/Hello-World.git",
        "ssh_url": "git@github.com:octocat/Hello-World.git",
        "svn_url": "https://svn.github.com/octocat/Hello-World",
        "mirror_url": "git://git.example.com/octocat/Hello-World",
        "homepage": "https://github.com",
        "language": "Java",
        "forks_count": 9,
        "stargazers_count": 80,
        "watchers_count": 80,
        "size": 108,
        "default_branch": "master",
        "open_issues_count": 0,
        "has_issues": True,
        "has_wiki": True,
        "has_downloads": True,
        "pushed_at": "2011-01-26T19:06:43Z",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2011-01-26T19:14:43Z",
        "permissions": {
            "admin": False,
            "push": False,
            "pull": True}}]
    repos_last_query = 'https://api.github.com/users/{}/repos'.format(
        ANOTHER_USER_LOGIN)
    repos_last_response = [{
        "id": 1296270,
        "owner": {
            "login": ANOTHER_USER_LOGIN,
            "id": 2,
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "gravatar_id": "somehexcode",
            "url": "https://api.github.com/users/octocat",
            "html_url": "https://github.com/octocat",
            "followers_url": "https://api.github.com/users/octocat/followers",
            "following_url": "whatever",
            "gists_url": "whatever",
            "starred_url": "whatever",
            "subscriptions_url": "whatever",
            "organizations_url": "https://api.github.com/users/octocat/orgs",
            "repos_url": "https://api.github.com/users/octocat/repos",
            "events_url": "whatever",
            "received_events_url": "whatever",
            "type": "User",
            "site_admin": False
            },
        "name": "Hello-World",
        "full_name": "octocat/Hello-World",
        "description": "This your first repo!",
        "private": False,
        "fork": False,
        "url": "https://api.github.com/repos/octocat/Hello-World",
        "html_url": "https://github.com/octocat/Hello-World",
        "clone_url": "https://github.com/octocat/Hello-World.git",
        "git_url": "git://github.com/octocat/Hello-World.git",
        "ssh_url": "git@github.com:octocat/Hello-World.git",
        "svn_url": "https://svn.github.com/octocat/Hello-World",
        "mirror_url": "git://git.example.com/octocat/Hello-World",
        "homepage": "https://github.com",
        "language": "Python",
        "forks_count": 9,
        "stargazers_count": 80,
        "watchers_count": 80,
        "size": 108,
        "default_branch": "master",
        "open_issues_count": 0,
        "has_issues": True,
        "has_wiki": True,
        "has_downloads": True,
        "pushed_at": "2011-01-26T19:06:43Z",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2011-01-26T19:14:43Z",
        "permissions": {
            "admin": False,
            "push": False,
            "pull": True}}]
    responses.add(
        responses.GET, user_query, match_querystring=True,
        body=json.dumps(users_response),
        adding_headers=user_links,
        status=200, content_type='application/json')
    responses.add(
        responses.GET, user_last_query, match_querystring=True,
        body=json.dumps(user_last_response),
        adding_headers=user_last_links,
        status=200, content_type='application/json')
    responses.add(
        responses.GET, repos_query, match_querystring=True,
        body=json.dumps(repos_response),
        status=200, content_type='application/json')
    responses.add(
        responses.GET, repos_last_query, match_querystring=True,
        body=json.dumps(repos_last_response),
        status=200, content_type='application/json')


@with_setup(setup)
@responses.activate
def test_search_users_per_country():
    user, password = 'fake', 'fake'
    result = main.search_users_per_country(user, password)
    expected = {"Spain": {"Java": 1, "Python": 1}}
    assert_equals(result, expected)


@with_setup(setup)
@responses.activate
def test_get_repos_for_user():
    user, password = 'fake', 'fake'
    counts = main.get_repos_for_user(user, password, USER_LOGIN)
    expected = {"Java": 1}
    assert_equals(dict(counts), expected)


@with_setup(setup)
@responses.activate
def test_get_all_users_for_country():
    user, password = 'fake', 'fake'
    user_logins = main.get_all_users_for_country(user, password, COUNTRY)
    assert_equals(user_logins, [USER_LOGIN, ANOTHER_USER_LOGIN])
