import json

cards = {}

for i in range(1,13):
    with open("data/raw/numberToValue" + str(i) + ".json", "r") as file:
        data = json.load(file)

    for key, value in data.items():
        cards[key] = value

with open("data/numberToValue.json", "w") as json_file:
    json.dump(cards, json_file, indent=4)
