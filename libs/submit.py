from bs4 import BeautifulSoup

from libs import connection


def get_submit_page_url(contest_url):
    top_page = connection.get_page_text(contest_url)
    soup = BeautifulSoup(top_page, "html.parser")
    list_items = soup.findAll("li")
    list_item = [item for item in list_items if "Submit" in item.getText()]
    href = list_item[0].select("a")[0].get("href")
    return contest_url + href[href.rfind("/"):]


def get_task_id(html, file_info):
    file_name = file_info[0]
    question_name = file_name[file_name.rfind("/") + 1:file_name.rfind(".")].upper()
    soup = BeautifulSoup(html, "html.parser")
    selects = soup.findAll("select")
    options = None
    for select in selects:
        if "task" in select["id"]:
            options = select.findAll("option")
            break
    if options is None:
        return None
    for option in options:
        if option.text.find(question_name) == 0:
            return option["value"]


def get_lang_id(html, file_info):
    extension = file_info[1]
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.findAll("div")
    options = None
    for div in divs:
        label = div.findAll("label")
        if len(label) != 0 and "Language" in label[0].text:
            options = div.findAll("option")
    if options is None:
        return None
    for option in options:
        lang = option.text
        if extension == ".cpp" and ("C++" in lang or "C&#43;&#43;" in lang) and "GCC" in lang:
            return option["value"]
        elif extension == ".py" and "Python3" in lang:
            return option["value"]
        elif extension == ".rb" and "Ruby" in lang:
            return option["value"]
    return None

    #     if ".cpp" == extension and :
    #         options = select.findAll("option")
    #         break
    # if options is None:
    #     return None
    # for option in options:
    #     if option.text.find(question_name) == 0:
    #         return option["value"]


def run(contest_url, file_info):
    if not contest_url:
        return False
    submit_url = get_submit_page_url(contest_url)
    submit_html = connection.get_page_text(submit_url)
    task_id = get_task_id(submit_html, file_info)
    print(task_id)
    lang_id = get_lang_id(submit_html, file_info)
    print(lang_id)
    return True


if __name__ == "__main__":
    run()
