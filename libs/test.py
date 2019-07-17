import pathlib
from subprocess import Popen, PIPE

from libs import directory


test_file_info = []


def search_example_files(question, condition):
    directory.change_directory(question)
    p = pathlib.Path(directory.current_directory)
    file_names = []
    for file in p.glob("test/*.txt"):
        if condition in file.name:
            file_names.append(file.resolve())
    directory.change_directory("../")
    return sorted(file_names)


def get_command():
    name = test_file_info[0]
    extension = test_file_info[1]
    if extension == ".cpp":
        return Popen([name[:name.rfind(".")]], shell=True, stdout=PIPE, stdin=PIPE)
    if extension == ".py" or extension == ".rb":
        return Popen([name], shell=True, stdout=PIPE, stdin=PIPE)
    return None


def test_for_one_sample(ex_input_file_name, ex_output_file_name):
    cmd = get_command()
    if cmd is None:
        return False


def run(file_info):
    global test_file_info
    if file_info is None:
        return False
    test_file_info = file_info

    file_name = file_info[0]
    question_name = file_name[file_name.rfind("/") + 1:file_name.rfind(".")].upper()
    input_file_names = search_example_files(question_name, "Input")
    output_file_names = search_example_files(question_name, "Output")
    if not len(input_file_names) == len(output_file_names):
        return False

    ac_count = 0
    wa_count = 0
    for index in range(len(input_file_names)):
        if test_for_one_sample(input_file_names[index], output_file_names[index]):
            ac_count += 1
        else:
            wa_count += 1

    if wa_count != 0:
        print(f"AC: {ac_count}")
        print(f"WA: {wa_count}")
        return False
    else:
        print(f"AC: {ac_count}")
        return True


if __name__ == "__main__":
    run(None)
