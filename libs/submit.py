from bs4 import BeautifulSoup

from libs import connection


def get_submit_page_url(contest_url):
    top_page = connection.get_page_text(contest_url)
    print(top_page)
    print()
    soup = BeautifulSoup(top_page, "html.parser")
    list_items = soup.findAll("li")
    list_item = [item for item in list_items if "Submit" in item.getText()]
    href = list_item[0].select("a")[0].get("href")
    return contest_url + href[href.rfind("/"):]


def run(contest_url, file_info):
    if not contest_url:
        return False
    submit_url = get_submit_page_url(contest_url)
    submit_html = connection.get_page_text(submit_url)
    print(submit_html)
    return True


if __name__ == "__main__":
    run()
