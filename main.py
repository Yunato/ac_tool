import sys
import directory
import re


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


if __name__ == '__main__':
    make_and_change_directory("AtCoder")
    contest_url = ""
    while True:
        print('Please input url of contest (ex. https://atcoder.jp/contests/xxx)')
        contest_url = input("Use 'exit' to exit\n")
        if contest_url == "exit":
            sys.exit()
        contest_name = extract_contest_name(contest_url)
        if contest_name is not None:
            break
    # TODO Plus, Get number and name of questions

    make_and_change_directory(contest_name)
    directory.print_working_directory()
    directory.copy_directory("../../template", "./QA")
    # TODO Rename file name when copying files from template
