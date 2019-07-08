import directory


def make_and_change_directory(dir_name):
    directory.make_directory(dir_name)
    directory.change_directory(dir_name)


if __name__ == '__main__':
    make_and_change_directory("AtCoder")
    # TODO Input URL top page of a contest
    # TODO Plus, Get number and name of questions
    contest_name = input('Please input contest name you want to join. (ex. ABC001)')
    print(contest_name)
    make_and_change_directory(contest_name)
    directory.print_working_directory()
    directory.copy_directory("../../template", "./QA")
    # TODO Rename file name when copying files from template
