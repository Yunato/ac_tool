from bs4 import BeautifulSoup
import json
import re
import requests
import sys

import directory


username = ""
password = ""


def read_user_info():
    global username, password
    if not directory.check_file("login_info.json"):
        sys.exit()
    json_data = json.load(open("login_info.json", "r"))
    username = json_data["username"]
    password = json_data["password"]


def make_and_change_directory(dir_name):
    directory.make_directory(dir_name)
    directory.change_directory(dir_name)


def extract_contest_name(url):
    pattern_alpha = r"^(http|https)://([\w-]+).contest.atcoder.(jp|jp/)?$"
    pattern_beta = r"^(http|https)://atcoder.jp/contests/([\w-]+)?(/)?$"
    match_alpha = re.search(pattern_alpha, url)
    match_beta = re.search(pattern_beta, url)

    if match_alpha is None and match_beta is None:
        print("This URL is incorrect\n")
        return None
    if match_beta is not None:
        return match_beta.group(2)
    if match_alpha is not None:
        return match_alpha.group(2)


def login_service():
    session = requests.session()
    login_info = {
        "username": username,
        "password": password
    }

    url_login = "https://atcoder.jp/login?continue=https%3A%2F%2Fatcoder.jp%2Fcontests%2Fabc131"
    response = session.get(url_login)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find(attrs={"name": "csrf_token"}).get("value")
    login_info["csrf_token"] = csrf_token
    res = session.post(url_login, data=login_info)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Can't login, so you mistake your username or password")
        sys.exit()
    print(res.text)


if __name__ == '__main__':
    read_user_info()
    make_and_change_directory("AtCoder")
    while True:
        print('Please input url of contest (ex. https://atcoder.jp/contests/xxx)')
        contest_url = input("Use 'exit' to exit\n")
        if contest_url == "exit":
            sys.exit()
        contest_name = extract_contest_name(contest_url)
        if contest_name is not None:
            break
    # TODO Plus, Get number and name of questions

    make_and_change_directory(contest_name)
    directory.print_working_directory()
    directory.copy_directory("../../template", "./QA")
    # TODO Rename file name when copying files from template
    login_service()
