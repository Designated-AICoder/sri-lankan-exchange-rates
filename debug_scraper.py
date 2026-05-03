# debug_table_structure.py
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get("https://www.nationstrust.com/foreign-exchange-rates", headers=headers, timeout=20)
soup = BeautifulSoup(resp.text, "html.parser")
table = soup.find("table", {"class": "table table-striped"})

print("=== FULL TABLE STRUCTURE ===")
for i, tr in enumerate(table.find_all("tr")):
    cols = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
    print(f"Row {i}: {cols}")

print("\n=== SEARCHING FOR USD RELATED TEXT ===")
# Let's search for any mention of USD in the entire page
usd_mentions = soup.find_all(string=lambda text: text and "USD" in text.upper())
print("USD mentions:", usd_mentions)

us_dollars_mentions = soup.find_all(string=lambda text: text and "US DOLLAR" in text.upper())
print("US DOLLAR mentions:", us_dollars_mentions)

print("\n=== ALL CURRENCY NAMES FOUND ===")
for tr in table.find_all("tr"):
    first_col = tr.find("td")
    if first_col:
        currency_name = first_col.get_text(strip=True)
        print(f"Currency: {currency_name}")