import sys
import join


hasJoined = False


def perform_joining():
    global hasJoined
    if not hasJoined and not join.run():
        sys.exit()
    hasJoined = True


def perform_build():
   print("build")


def perform_submitting():
    print("submit")


def perform_change_contest():
    global hasJoined
    print("Change contest")
    join.reset()
    hasJoined = False



if __name__ == "__main__":    
    try:
        while True:
            perform_joining()
            print("Please input any of the following commands")
            print("- build  : If this commnad is inputed or If empty, run Build & Submit")
            print("- change : You can select a contest again")
            print("- exit   : This tool will be exited")
            cmd = input()
            print()

            cmd = cmd.lower()
            if cmd == "build" or cmd == "":
                perform_build()
                perform_submitting()
            elif cmd == "change":
                perform_change_contest()
            elif cmd == "exit":
                sys.exit()
            print()
    except KeyboardInterrupt:
        sys.exit()
