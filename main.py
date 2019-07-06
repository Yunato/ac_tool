import os


current_directory = ""


def say_hello():
    print("Hello, World!")


def print_directory():
    directories = os.listdir(current_directory)
    print(directories)


def get_current_directory():
    global current_directory
    current_directory = os.getcwd()
    print(current_directory)


def make_directory(dir_name):
    global current_directory
    new_directory = current_directory + "/" + dir_name
    if not os.path.isdir(new_directory):
        print(new_directory)
        os.mkdir(new_directory)
    else:
        print(f"\"{dir_name}\" is already exist at {current_directory}.")


if __name__ == '__main__':
    say_hello()
    get_current_directory()
    print_directory()
    make_directory("AtCoder")
    print_directory()
