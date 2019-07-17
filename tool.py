import sys

from libs import login, join, build, test

hasJoined = False


def perform_joining():
    global hasJoined
    if not hasJoined and not join.run():
        sys.exit()
    hasJoined = True


def perform_building():
    return build.run()


def perform_testing(file_info):
    test.run(file_info)


def perform_submitting():
    print("submit")
    # submit.run()


def perform_change_contest():
    global hasJoined
    print("Change contest")
    join.reset()
    hasJoined = False


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
            print()

            cmd = cmd.lower()
            if cmd == "change":
                perform_change_contest()
            elif cmd == "exit":
                sys.exit()
            else:
                file_info = perform_building()
                if file_info is None or not perform_testing(file_info):
                    continue
                perform_submitting()
    except KeyboardInterrupt:
        sys.exit()
