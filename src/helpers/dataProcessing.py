import json
import os


def saveDataToJson(filename, data):
    os.makedirs(os.path.dirname(f"src/exam/{filename}"), exist_ok=True)

    with open(f"src/exam/{filename}", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.close()


def getJson(filename):
    try:
        with open(f"src/exam/{filename}.json", "r") as f:
            data = json.load(f)
            f.close()
        return data
    except FileNotFoundError:
        print(f"File {filename}.json not found")
        return []
