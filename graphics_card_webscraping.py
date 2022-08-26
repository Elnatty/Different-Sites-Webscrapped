from bs4 import BeautifulSoup
import requests
import re       # regular expression

search_term = input("what product do you want to search for? ")
url = requests.get(f"https://www.newegg.com/p/pl?d={search_term}").text
doc = BeautifulSoup(url, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
# split the result in order to get the page number.
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])
# looping through and getting all elements in all pages
items_found = {}
for page in range(1, pages+1):
    url = requests.get(f"https://www.newegg.com/p/pl?d={search_term}&page={page}").text
    doc = BeautifulSoup(url, "html.parser")

    div = doc.find(class_= "item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    # text=re.compile() to search for keyword --> "user input term"
    items = doc.find_all(text=re.compile(search_term))
    try:
        for item in items:
            parent = item.parent
            if parent.name != "a":
                continue
            link = parent["href"]
            next_parent = item.find_parent(class_="item-container")
            price = next_parent.find(class_="price-current").strong.string

            items_found[item] = {"price": int(price.replace(",", "")), "link": link}
    except:
        pass
# print(items_found)
# sorting all the items by their prices to get a nicer output..
import pandas
sorted_items = sorted(items_found.items(), key=lambda x: x[1]["price"])      # this gives a tuple with each key and value in it.
for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]["link"])
