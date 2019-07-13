from bs4 import BeautifulSoup
import requests


username = ""
password = ""


def set_user_info(name, pwd):
    global username, password
    username = name
    password = pwd


def login_service():
    session = requests.session()
    login_url = "https://atcoder.jp/login?continue=https%3A%2F%2Fatcoder.jp%2Fcontests%2Fabc131"
    login_info = {
        "username": username,
        "password": password
    }

    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.text, "html.parser")
    csrf_token = soup.find(attrs={"name": "csrf_token"}).get("value")
    login_info["csrf_token"] = csrf_token
    # TODO: This statement can't return top_page text
    top_page = session.post(login_url, data=login_info)
    try:
        top_page.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Can't login, so you mistake your username or password")
        return None
    print(top_page.text)
    return top_page.text


def get_page_info(url):
    page_info = requests.get(url)
    return page_info.text
