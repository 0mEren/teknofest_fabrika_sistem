import json

file_path = "test.json"

with open(file_path, "r", encoding='utf-8') as file:
    data = json.load(file)

data["baslangic"] = 0

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent = 4)
