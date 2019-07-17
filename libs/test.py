import pathlib
from subprocess import Popen, PIPE

from libs import directory


def get_command(name, ext):
    if ext == ".cpp":
        return Popen([name[:name.rfind(".")]], shell=True, stdout=PIPE, stdin=PIPE)
    if ext == ".py" or ext == ".rb":
        return Popen([name], shell=True, stdout=PIPE, stdin=PIPE)
    return None


def run(file_info):
    if file_info is None:
        return False
    file_name = file_info[0]
    extension = file_info[1]
    cmd = get_command(name=file_name, ext=extension)
    if cmd is None:
        return False
    return True


if __name__ == "__main__":
    run(None)
