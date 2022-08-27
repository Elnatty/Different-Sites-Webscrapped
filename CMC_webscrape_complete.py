import requests
import pandas as pd
from bs4 import BeautifulSoup

r = requests.get("https://coinmarketcap.com")
soup = BeautifulSoup(r.text, "lxml")
# ----------------------------------> iterate through all pages.
# pages = soup.find("div", class_="sc-16r8icm-0 sc-4r7b5t-0 gJbsQH").p.text.split(" ")[-1]

full_dict = {}
for total in range(1, 2):
    url_ = requests.get(f"https://coinmarketcap.com/?page={total}")
    soup = BeautifulSoup(url_.text, "lxml")

    # --------------------------> sorting coins from 1 - 10
    from_1_10 = soup.tbody.contents  # from 1 - 10
    from_1_to_10_dict = {}
    try:
        for tr in from_1_10:
            # looping through every data inside each table row
            name, price = tr.contents[2:4]
            fixed_name = name.p.text
            fixed_price = price.span.text
            from_1_to_10_dict[fixed_name] = fixed_price
    except:
        pass

    # --------------------------> sorting coins from 11 - 100
    from_11_100 = soup.find_all("tr")  # from 11 - 100
    from_11_to_100_dict = {}
    for items in from_11_100[11:]:
        title = items.text.split("$")
        from_11_to_100_dict[title[0]] = "$"+title[1]
    # merging both dict
    from_1_to_10_dict.update(from_11_to_100_dict)
    full_dict.update(from_1_to_10_dict)
# print(full_dict)
df = pd.DataFrame(list(full_dict.items()), columns=["Coin", "Price"])
df.to_csv("coinmarketcap.csv", index=False)
print(df.head(10))