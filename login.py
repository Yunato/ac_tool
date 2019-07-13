import directory
import connection
import json


def read_user_info():
    if not directory.check_file("login_info.json"):
        print("Not found login_info.json")
        return False
    json_data = json.load(open("login_info.json", "r"))
    connection.set_user_info(json_data["username"], json_data["password"])
    return True


def run():
    if not read_user_info():
        return False
    # connection.login_service()
    return True


if __name__ == "__main__":
    run()
