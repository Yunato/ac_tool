from bs4 import BeautifulSoup
import requests
import sys


username = ""
password = ""


def set_user_info(name, pwd):
    global username, password
    username = name
    password = pwd


def login_service():
    session = requests.session()
    login_info = {
        "username": username,
        "password": password
    }

    url_login = "https://atcoder.jp/login?continue=https%3A%2F%2Fatcoder.jp%2Fcontests%2Fabc131"
    login_page = session.get(url_login)
    soup = BeautifulSoup(login_page.text, "html.parser")
    csrf_token = soup.find(attrs={"name": "csrf_token"}).get("value")
    login_info["csrf_token"] = csrf_token
    top_page = session.post(url_login, data=login_info)
    try:
        top_page.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Can't login, so you mistake your username or password")
        sys.exit()
    print(top_page.text)
    return top_page.text


def get_page_info(url):
    page_info = requests.get(url)
    return page_info.text


def get_question_name(html):
    questions = []
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    index = -1
    for i in range(len(tables)):
        th = tables[i].findAll("th")
        if "Task" in th[0]:
            index = i
            break
    if index == -1:
        return questions
    for tr in tables[index].findAll("tr"):
        tds = tr.select("td")
        if len(tds) == 2:
            questions.append(tds[0].text)
    return questions
