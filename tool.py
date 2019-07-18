import sys

from libs import login, join, build, test, submit

contest_url = ""


def perform_joining():
    global contest_url
    if not contest_url:
        contest_url = join.run()
        if contest_url is None:
            sys.exit()


def perform_building():
    return build.run()


def perform_testing(file_info):
    return test.run(file_info)


def perform_submitting(file_info):
    global contest_url
    submit.run(contest_url, file_info)


def perform_change_contest():
    global contest_url
    print("Change contest")
    join.reset()
    contest_url = ""


if __name__ == "__main__":
    if not login.run():
        sys.exit()
    try:
        while True:
            perform_joining()
            print()
            print("Please input any of the following commands")
            print("- change : You can select a contest again")
            print("- exit   : This tool will be exited")
            print("If other command is inputted or if empty, run Build & Test & Submit")
            cmd = input()
            if cmd != "":
                print()

            cmd = cmd.lower()
            if cmd == "change":
                perform_change_contest()
            elif cmd == "exit":
                sys.exit()
            else:
                exec_file_info = perform_building()
                if exec_file_info is None or not perform_testing(exec_file_info):
                    continue
                perform_submitting(exec_file_info)
    except KeyboardInterrupt:
        sys.exit()
