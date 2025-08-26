import json
file_path = "../text_for_analysis/songs_TheBeatles.json"
def read_json():
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except:
        data = {}
        return data

songs_data = read_json()
songs_list = songs_data["songs"]

print(len(songs_list))