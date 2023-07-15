import json


def database_update(minutie_data, login):
    new_data = {login: minutie_data}

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        with open("data.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)
    else:
        data.update(new_data)

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)


def database_load():
    with open("data.json", "r") as data_file:
        data = json.load(data_file)

    return data

