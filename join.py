import json
import re

import connection
import directory


root_path = directory.print_working_directory()


def read_user_info():
    if not directory.check_file("login_info.json"):
        print("Not found login_info.json")
        return False
    json_data = json.load(open("login_info.json", "r"))
    connection.set_user_info(json_data["username"], json_data["password"])
    return True


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


def reset():
    directory.current_directory = root_path


def run():
    if not read_user_info():
        return False
    make_and_change_directory("AtCoder")
    try:
        while True:
            print('Please input url of contest (ex. https://atcoder.jp/contests/xxx)')
            contest_url = input("Use 'exit' to exit\n")
            if contest_url == "exit":
                return False
            contest_name = extract_contest_name(contest_url)
            if contest_name is not None:
                break
    except KeyboardInterrupt:
        return False
    make_and_change_directory(contest_name)
    # connection.login_service()
    top_page_info = connection.get_page_info(contest_url)
    create_directory_of_question(top_page_info)
    rename_answer_files_each_directory()
    print(f"Successful in joining at {contest_name}!!\n")
    return True


if __name__ == '__main__':
    run()
