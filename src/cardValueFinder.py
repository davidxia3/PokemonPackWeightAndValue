from selenium import webdriver  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import random
import time
import json

cards = {}

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)

page = 1

driver.get("https://www.tcgplayer.com/search/pokemon/sv04-paradox-rift?view=grid&productLineName=pokemon&setName=sv04-paradox-rift&ProductTypeName=Cards&page=" + str(page))

delay = random.uniform(3,5)
time.sleep(delay)


searchResults = driver.find_element(By.CLASS_NAME, "search-results").find_elements(By.CLASS_NAME, "search-result")

links = []

for searchResult in searchResults:
    link = searchResult.find_element(By.CLASS_NAME, "search-result__content").find_element(By.TAG_NAME, "a").get_attribute("href")
    links.append(link)

for link in links:
    driver.get(link)

    delay = random.uniform(3,5)
    time.sleep(delay)


    headers = {
        "base": [-1,0],
        "holo": [-1,0],
        "reverse": [-1,0]
    }

    chart = driver.find_element(By.CLASS_NAME, "chart-container")
    tableHead = chart.find_element(By.TAG_NAME, "thead").find_element(By.TAG_NAME, "tr").find_elements(By.TAG_NAME, "th")

    
    for i in range(1, len(tableHead)):
        text = driver.execute_script("return arguments[0].textContent;", tableHead[i])
        if text == "Normal":
            headers["base"][0] = i
        elif text == "Holofoil":
            headers["holo"][0] = i
        elif text == "Reverse Holofoil":
            headers["reverse"][0] = i
    

    tableRows = chart.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")[-1].find_elements(By.TAG_NAME, "td")

    for value in headers.values():
        if value[0] != -1:
            text = driver.execute_script("return arguments[0].textContent;", tableRows[value[0]])
            value[1] = float(text[1:])
    

    details = driver.find_element(By.CLASS_NAME, "product__item-details__attributes")
    info = details.find_element(By.TAG_NAME, "li").find_element(By.TAG_NAME, "span").text

    if info.find("Code Card") != -1:
        name = driver.find_element(By.CLASS_NAME, "product-details__name").text
        number = name
    else:
        number = info.split("/")[0]

    cards[number] = {
        "base": headers["base"][1],
        "holo": headers["holo"][1],
        "reverse": headers["reverse"][1]
    }



with open("data/raw/numberToValue" + str(page) + ".json", "w") as file:
    json.dump(cards, file, indent=4)






