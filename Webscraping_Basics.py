from bs4 import BeautifulSoup
import requests

url = requests.get("https://coinmarketcap.com/").text
soup = BeautifulSoup(url, "html.parser")

tbody = soup.tbody.contents
prices = {}
try:
    for tr in tbody:
        # looping through every data inside each table row
        name, price = tr.contents[2:4]
        fixed_name = name.p.text
        fixed_price = price.span.text
        prices[fixed_name] = fixed_price
except:
    pass
for p, q in prices.items():
    print(f"{p}: {q}")