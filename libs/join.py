from bs4 import BeautifulSoup
import collections as cl
import json
import os
import pathlib
import re

from libs import directory, connection

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
    tasks_url = get_tasks_page_url(contest_url)
    tasks_html = connection.get_page_text(tasks_url)
    questions = get_ques_name_and_url(tasks_html)
    root = get_root_url(contest_url)
    for question in questions:
        directory.copy_directory("../../template", f"./{question[0]}")
        directory.change_directory(question[0])
        question_html = connection.get_page_text(f"{root}{question[1]}")
        examples = extract_example(question_html)
        create_example_files(examples)
        directory.change_directory("../")


def get_tasks_page_url(contest_url):
    top_page = connection.get_page_text(contest_url)
    soup = BeautifulSoup(top_page, "html.parser")
    list_items = soup.findAll("li")
    list_item = [item for item in list_items if "Tasks" in item.getText()]
    href = list_item[0].select("a")[0].get("href")
    return contest_url + href[href.rfind("/"):]


def get_ques_name_and_url(html):
    questions = []
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select("table")[0]
    for tr in table.findAll("tr"):
        tds = tr.select("td")
        if tds:
            href = tds[0].select("a")[0].get("href")
            questions.append([tds[0].text, href])
    return questions


def get_root_url(contest_url):
    root = contest_url
    index = root.find("/", len("https://"))
    if not index == -1:
        root = root[:index]
    return root


def extract_example(html):
    examples = []
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.findAll("section")
    for section in sections:
        h3 = section.select("h3")
        pre = section.select("pre")
        if "Sample" in h3[0].text:
            examples.append([h3[0].text, pre[0].text])
    return examples


def create_example_files(file_info):
    make_and_change_directory("test")
    for info in file_info:
        file_name = f"{directory.current_directory}/{info[0].replace(' ', '_')}"
        file_name += ".txt"
        with open(file_name, "w") as f:
            f.write(info[1])
    directory.change_directory("../")


def rename_answer_files_each_directory():
    for sub_dir in directory.list_content():
        if os.path.isfile(f"{directory.current_directory}/{sub_dir}"):
            continue
        directory.change_directory(sub_dir)
        question_name = sub_dir.lower()
        for file in directory.list_content():
            if not os.path.isfile(f"{directory.current_directory}/{file}"):
                continue
            extension = file[file.rfind("."):]
            directory.rename_file(file, question_name + extension)
        directory.change_directory("../")


def create_info_json():
    file_name = f"{directory.current_directory}/info.json"
    if not os.path.exists(file_name):
        stamp = get_stamp_from_source_files()
        with open(file_name, "w") as f:
            data = cl.OrderedDict()
            data["stamp"] = stamp
            json.dump(data, f, indent=2)


def get_stamp_from_source_files():
    p = pathlib.Path(directory.current_directory)
    stamp = None
    for file in p.glob("**/*[!.txt]"):
        if file.is_file() and (stamp is None or stamp.stat().st_mtime < file.stat().st_mtime):
            stamp = file
    return stamp.stat().st_mtime


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
    if contest_url[len(contest_url) - 1] == "/":
        contest_url = contest_url[:len(contest_url) - 1]
    make_and_change_directory(contest_name)
    create_directory_of_question(contest_url)
    rename_answer_files_each_directory()
    create_info_json()
    print(f"Successful in joining at {contest_name}!!\n")
    return True


if __name__ == '__main__':
    run()
