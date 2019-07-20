from bs4 import BeautifulSoup
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
