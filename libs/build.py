import json
import os
import pathlib

from libs import directory


def get_stamp_from_source_files():
    p = pathlib.Path(directory.current_directory)
    stamp = None
    for file in p.glob("**/*[!.txt|!.json]"):
        if not file.is_dir() and file.is_file() and \
                (stamp is None or stamp.stat().st_mtime < file.stat().st_mtime):
            stamp = file
    return stamp.stat().st_mtime


def read_info_json():
    file_name = f"{directory.current_directory}/info.json"
    if os.path.exists(file_name):
        json_data = json.load(open(file_name, "r"))
        return json_data["stamp"]
    return 0


def run(has_checked=False):
    if not has_checked:
        old_stamp = read_info_json()
        new_stamp = get_stamp_from_source_files()
        if old_stamp == new_stamp:
            print("The newest source file is already built last time")
            print("So, You didn't change any source files")
            return False
        return True


if __name__ == "__main__":
    run(True)
