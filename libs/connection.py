from bs4 import BeautifulSoup
import re
import requests


session = requests.session()
username = ""
password = ""


def set_user_info(name, pwd):
    global username, password
    username = name
    password = pwd


def login_alpha_service():
    login_url = "https://abc001.contest.atcoder.jp/login"
    login_info = {
        "name": username,
        "password": password
    }

    top_page = session.post(login_url, data=login_info)
    try:
        top_page.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Can't login, so you mistake your username or password")
        return None


def login_beta_service():
    login_url = "https://atcoder.jp/login"
    login_info = {
        "username": username,
        "password": password
    }

    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.text, "html.parser")
    csrf_token = soup.find(attrs={"name": "csrf_token"}).get("value")
    login_info["csrf_token"] = csrf_token
    top_page = session.post(login_url, data=login_info)
    try:
        top_page.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Can't login, so you mistake your username or password")
        return None


def get_page_text(url):
    page_info = session.get(url)
    return page_info.text


def submit(contest_url, html, task_id, lang_id, source_code):
    pattern_alpha = r"^(http|https)://([\w-]+).contest.atcoder.(jp|jp/)?"
    pattern_beta = r"^(http|https)://atcoder.jp/contests/([\w-]+)?(/)?"
    match_alpha = re.search(pattern_alpha, contest_url)
    match_beta = re.search(pattern_beta, contest_url)

    if match_alpha is None and match_beta is None:
        return "Failed"
    if match_alpha is not None:
        return submit_alpha_service(contest_url, html, task_id, lang_id, source_code)
    if match_beta is not None:
        return submit_beta_service(contest_url, html, task_id, lang_id, source_code)


def submit_alpha_service(contest_url, html, task_id, lang_id, source_code):
    submit_info = {
        "task_id": task_id,
        "language_id_731": lang_id,
        "source_code": source_code
    }

    soup = BeautifulSoup(html, "html.parser")
    session_id = soup.find(attrs={"name": "__session"}).get("value")
    submit_info["__session"] = session_id
    result = session.post(contest_url, data=submit_info)
    try:
        result.raise_for_status()
        if result.status_code == 200:
            return "Success"
        else:
            return "Failed"
    except requests.exceptions.HTTPError:
        return "Failed"


def submit_beta_service(contest_url, html, task_id, lang_id, source_code):
    submit_info = {
        "data.TaskScreenName": task_id,
        "data.LanguageId": lang_id,
        "sourceCode": source_code
    }

    soup = BeautifulSoup(html, "html.parser")
    csrf_token = soup.find(attrs={"name": "csrf_token"}).get("value")
    submit_info["csrf_token"] = csrf_token
    result = session.post(contest_url, data=submit_info)
    try:
        result.raise_for_status()
        if result.status_code == 200:
            return "Success"
        else:
            return "Failed"
    except requests.exceptions.HTTPError:
        return "Failed"
