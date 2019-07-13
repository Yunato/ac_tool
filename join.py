from bs4 import BeautifulSoup
import re

import connection
import directory


root_path = directory.current_directory


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


def create_directory_of_question(contest_url):
    top_page = connection.get_page_text(contest_url)
    soup = BeautifulSoup(top_page, "html.parser")
    list_items = soup.findAll("li")
    list_item = [item for item in list_items if "Tasks" in item.getText()]
    href = list_item[0].select("a")[0].get("href")
    tasks_url = contest_url + href[href.rfind("/"):]

    questions = get_question_name(tasks_url)
    for question in questions:
        directory.copy_directory("../../template", f"./{question}")


def get_question_name(tasks_url):
    questions = []
    html = connection.get_page_text(tasks_url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("table")[0]
    for tr in table.findAll("tr"):
        tds = tr.select("td")
        if tds:
            questions.append(tds[0].text)
    return questions


def rename_answer_files_each_directory():
    for sub_dir in directory.list_content():
        directory.change_directory(sub_dir)
        question_name = sub_dir.lower()
        for file in directory.list_content():
            extension = file[file.rfind("."):]
            directory.rename_file(file, question_name + extension)
        directory.change_directory("../")


def reset():
    directory.current_directory = root_path


def run():
    make_and_change_directory("AtCoder")
    while True:
        print('Please input url of contest (ex. https://atcoder.jp/contests/xxx)')
        contest_url = input("Use 'exit' to exit\n")
        if contest_url == "exit":
            return False
        contest_name = extract_contest_name(contest_url)
        if contest_name is not None:
            break
    make_and_change_directory(contest_name)
    create_directory_of_question(contest_url)
    rename_answer_files_each_directory()
    print(f"Successful in joining at {contest_name}!!\n")
    return True


if __name__ == '__main__':
    run()
