import os
import shutil


current_directory = ""


def say_hello():
    print("Hello, World!")


def println(msg):
    output = msg if type(msg) == str else "\n".join(msg)
    print(output + "\n")


def print_directory():
    print("ls")
    directories = os.listdir(current_directory)
    println(directories)


def get_current_directory():
    global current_directory
    print("pwd")
    current_directory = os.getcwd()
    println(current_directory)


def make_directory(dir_name):
    global current_directory
    print(f"mkdir {dir_name}")
    new_directory = current_directory + "/" + dir_name
    if not os.path.isdir(new_directory):
        println(new_directory)
        os.mkdir(new_directory)
    else:
        println(f"\"{dir_name}\" is already exist at {current_directory}.")


def change_directory(dir_name):
    global current_directory
    print(f"cd {dir_name}")
    current_directory += "/" + dir_name


def copy_directory(source_dir, target_dir):
    global current_directory
    print(f"cp {source_dir} {target_dir}")
    shutil.copytree(source_dir, target_dir)


if __name__ == '__main__':
    while True:
        cmd = input().split()
        if cmd[0] == "ls":
            print_directory()
        elif cmd[0] == "pwd":
            get_current_directory()
        elif cmd[0] == "mkdir":
            make_directory(cmd[1])
        elif cmd[0] == "cd":
            change_directory(cmd[1])
        elif cmd[0] == "cp":
            copy_directory(cmd[1], cmd[2])
        else:
            println("Not found")
