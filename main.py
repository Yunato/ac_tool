import os


def say_hello():
    print("Hello, World!")


def print_directory():
    directory = os.listdir()
    print(directory)


if __name__ == '__main__':
    say_hello()
    print_directory()
