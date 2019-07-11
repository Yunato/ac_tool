import json
import re
import sys

import connection
import directory


def read_user_info():
    if not directory.check_file("login_info.json"):
        print("Not found login_info.json")
        sys.exit()
    json_data = json.load(open("login_info.json", "r"))
    connection.set_user_info(json_data["username"], json_data["password"])


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


def create_directory_of_question(html):
    questions = connection.get_question_name(html)
    for question in questions:
        directory.copy_directory("../../template", f"./{question}")


def rename_answer_files_each_directory():
    for sub_dir in directory.list_content():
        directory.change_directory(sub_dir)
        question_name = sub_dir.lower()
        for file in directory.list_content():
            extension = file[file.rfind("."):]
            directory.rename_file(file, question_name + extension)
        directory.change_directory("../")


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
    make_and_change_directory(contest_name)
    response = connection.login_service()
    create_directory_of_question(response)
    rename_answer_files_each_directory()

