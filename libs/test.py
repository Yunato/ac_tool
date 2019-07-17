import pathlib
from subprocess import Popen, PIPE

from libs import directory


def get_command(name, ext):
    if ext == ".cpp":
        return Popen([name[:name.rfind(".")]], shell=True, stdout=PIPE, stdin=PIPE)
    if ext == ".py" or ext == ".rb":
        return Popen([name], shell=True, stdout=PIPE, stdin=PIPE)
    return None


def test(cmd, file_name):
    question = file_name[file_name.rfind("/") + 1:file_name.rfind(".")].upper()
    print(question)
    print(search_files(question, "Input"))
    print(search_files(question, "Output"))


def search_example_files(question, condition):
    directory.change_directory(question)
    p = pathlib.Path(directory.current_directory)
    files = []
    for file in p.glob("test/*.txt"):
        if condition in file.name:
            files.append(file)
    directory.change_directory("../")
    return files


def run(file_info):
    if file_info is None:
        return False
    file_name = file_info[0]
    extension = file_info[1]
    cmd = get_command(name=file_name, ext=extension)
    if cmd is None:
        return False
    test(cmd, file_name)
    return True


if __name__ == "__main__":
    run(None)
