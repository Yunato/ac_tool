import os
import shutil
import logging


# logging.basicConfig(level=logging.DEBUG)
current_directory = os.getcwd()
__mode = True


def get_absolute_path(path):
    global current_directory
    directories = path.split("/")
    rtn_directory = current_directory
    for directory in directories:
        if directory == "":
            continue
        elif directory == "..":
            last_index = rtn_directory.rfind("/")
            rtn_directory = rtn_directory[:last_index]
        else:
            rtn_directory += "/" + directory
    return rtn_directory


def println(msg):
    output = msg if type(msg) == str else "\n".join(msg)
    print(output + "\n")


def list_directory():
    logging.debug("ls")
    directories = os.listdir(current_directory)
    println(directories)


def print_working_directory():
    global current_directory
    logging.debug("pwd")
    # current_directory = os.getcwd()
    println(current_directory)


def make_directory(dir_name):
    global current_directory
    logging.debug(f"mkdir {dir_name}")
    new_directory = current_directory + "/" + dir_name
    if not os.path.isdir(new_directory):
        os.mkdir(new_directory)
    elif __mode:
        logging.debug(f"A directory with name \"{dir_name}\" already exists at {current_directory}")


def change_directory(dir_name):
    global current_directory
    logging.debug(f"cd {dir_name}")
    next_directory = current_directory + "/" + dir_name
    if os.path.isdir(next_directory):
        current_directory = next_directory
    elif __mode:
        println(f"No such directory: {dir_name}")


def copy_directory(source_dir, target_dir):
    global current_directory
    logging.debug(f"cp {source_dir} {target_dir}")
    absolute_source_path = get_absolute_path(source_dir)
    absolute_target_path = get_absolute_path(target_dir)
    if os.path.isdir(absolute_source_path):
        shutil.copytree(absolute_source_path, absolute_target_path)
    elif __mode:
        println(f"No such directory: {absolute_source_path}")


def check_file(file_name):
    global current_directory
    logging.debug(f"exist {file_name}")
    target_path = current_directory + "/" + file_name
    if os.path.isfile(target_path):
        return True
    else:
        println(f"A file with name \"{file_name}\" not found")
        return False


if __name__ == '__main__':
    __mode = True
    while True:
        cmd = input().split()
        if cmd[0] == "ls":
            list_directory()
        elif cmd[0] == "pwd":
            print_working_directory()
        elif cmd[0] == "mkdir":
            if len(cmd) == 2:
                make_directory(cmd[1])
            else:
                println(f"usage: mkdir directory")
        elif cmd[0] == "cd":
            if len(cmd) == 2:
                change_directory(cmd[1])
            else:
                println(f"usage: cd directory")
        elif cmd[0] == "cp":
            if len(cmd) == 3:
                copy_directory(cmd[1], cmd[2])
            else:
                println(f"usage: cp source_directory target_directory")
        elif cmd[0] == "exist":
            if len(cmd) == 2:
                check_file(cmd[1])
            else:
                println(f"usage: exist file")
        elif cmd[0] == "exit":
            break
        else:
            println(f"Command not found: {cmd[0]}")
