import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = "https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1"

# getting total content counts.
def total_count(url):
    r = requests.get(url)
    data = r.json()
    totalresults = data["total_count"]
    return int(totalresults)
# print(total_count(url))

# --------------------> 1 getting the data.
def get_data(url):
    r = requests.get(url)
    data = r.json()
    return data["results_html"]

# --------------------> parse data with BeautifulSoup
def parse(data):
    gameslist = []
    soup = BeautifulSoup(data, "html.parser")
    games = soup.find_all("a")
    for game in games:
        title = game.find("span", class_="title").text
        try:
            price = game.find("div", class_="search_price").text.strip().split("$")[1]
        except:
            pass
        try:
            discprice = game.find("div", class_="search_price").text.strip().split("$")[2]
        except:
            discprice = price
        # print(f"{title} --> {price}, {discprice}")
        my_game = {"title": title, "price": price, "dicounted price": discprice}
        gameslist.append(my_game)
    return gameslist

# --------------------> saving output into csv file with pandas.
def output(results):
    # list comprehension to nicely arrange data from different pages
    gamesdf = pd.concat([pd.DataFrame(g) for g in results])
    gamesdf.to_csv("gamesprices.csv", index=False)
    # print(gamesdf.head())       # print 1st 5 results
    return

# data = get_data(url)
# gameslist = parse(data)
# output(gameslist)

results = []
for x in range(0, total_count(url), 50):
    data = get_data(f"https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1")
    results.append(parse(data))
output(results)