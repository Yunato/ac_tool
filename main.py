import directory


__require_keyword = "atcoder.jp"


def make_and_change_directory(dir_name):
    directory.make_directory(dir_name)
    directory.change_directory(dir_name)


def validate_url(url):
    if __require_keyword in url:
        return True
    else:
        return False


# TODO  Correspond to below format: https://xxx.contest.atcoder.jp/
def extract_contest_name(url):
    separated = url.split("/")
    return separated[4]


if __name__ == '__main__':
    make_and_change_directory("AtCoder")
    contest_url = ""
    # TODO Exit
    while not validate_url(contest_url):
        print('Please input url of contest (ex. https://atcoder.jp/contests/xxx)\n')
        contest_url = input("'Use exit() to exit'\n")
    contest_name = extract_contest_name(contest_url)
    print(contest_name)
    # TODO Plus, Get number and name of questions

    make_and_change_directory(contest_name)
    directory.print_working_directory()
    directory.copy_directory("../../template", "./QA")
    # TODO Rename file name when copying files from template
