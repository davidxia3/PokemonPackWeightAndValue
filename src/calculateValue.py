import csv
import json

CODECARD = "Code Card - Paradox Rift Booster Pack - SV04: Paradox Rift (SV04)"

with open("data/numberToValue.json", "r") as file:
    cards = json.load(file)


def getCardValue(num):
    number = num.lstrip("0")
    type = "base"
    if number[-1] == "R":
        number = number[:-1]
        type = "reverse"
    elif number[-1] == "H":
        number = number[:-1]
        type = "holo"
    
    cardValues = cards[number]
    return cardValues[type]

    
weights = []
values = []

with open("" , "r") as file:
    packs = csv.DictReader(file)

    for pack in packs:
        total = 0

        for i in range(1, 11):
            cardNum = pack["card" + str(i)]
            total = total + getCardValue(cardNum)

        total = total + getCardValue(CODECARD)

        weight = pack["weight"]

        weights.append(weight)
        values.append(total)


