import os


current_directory = ""


def say_hello():
    print("Hello, World!")


def println(msg):
    output = msg if type(msg) == str else " ".join(msg)
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
    print("mkdir")
    new_directory = current_directory + "/" + dir_name
    if not os.path.isdir(new_directory):
        println(new_directory)
        os.mkdir(new_directory)
    else:
        println(f"\"{dir_name}\" is already exist at {current_directory}.")


if __name__ == '__main__':
    get_current_directory()
    print_directory()
    make_directory("AtCoder")
    print_directory()
