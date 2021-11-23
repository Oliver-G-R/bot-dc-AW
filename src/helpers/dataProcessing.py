import json


def save_to_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
        f.close()
