import collections as cl
import json
import os
import pathlib
import subprocess

from libs import directory


def get_newest_source_file():
    p = pathlib.Path(directory.current_directory)
    newest_file = None
    for file in p.glob("**/*.*[!.txt|!.json]"):
        if not file.is_dir() and file.is_file() and \
                (newest_file is None or newest_file.stat().st_mtime < file.stat().st_mtime):
            newest_file = file
    return newest_file


def check_updated_newest_file(newest_file):
    old_stamp = read_info_json()
    new_stamp = newest_file.stat().st_mtime
    if old_stamp == new_stamp:
        print("<<< Warning >>>")
        print("The newest source file is already built last time")
        print("So, You didn't change any source files")
        print("If you change any source files, please save them at your editor")
        return False
    return True


def read_info_json():
    file_name = f"{directory.current_directory}/info.json"
    if os.path.exists(file_name):
        json_data = json.load(open(file_name, "r"))
        return json_data["stamp"]
    return 0


def update_info_json(file):
    stamp = file.stat().st_mtime
    file_name = f"{directory.current_directory}/info.json"
    with open(file_name, "w") as f:
        data = cl.OrderedDict()
        data["stamp"] = stamp
        json.dump(data, f, indent=2)


def build(name, ext):
    if ext == ".cpp":
        try:
            output_name = name[:name.rfind(".")]
            print(f"Executable file: {output_name}")
            args = ["g++", "-o", output_name, name]
            subprocess.check_call(args)
        except subprocess.CalledProcessError:
            print("Failed in building")
            return None
        print("Successful in building")
        return [name, ext]
    if ext == ".py" or ext == ".rb":
        return [name, ext]
    return None


def run(has_checked=False):
    newest_file = get_newest_source_file()
    if not has_checked:
        if not check_updated_newest_file(newest_file):
            return None
    update_info_json(newest_file)
    file_name = str(newest_file.resolve())
    extension = file_name[file_name.rfind("."):]
    return build(name=file_name, ext=extension)


if __name__ == "__main__":
    run(True)
