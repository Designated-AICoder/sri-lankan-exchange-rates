# scrapers/nations_trust.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, UTC
import re

NTB_URL = "https://www.nationstrust.com/foreign-exchange-rates"

def fetch_nations_trust_rates() -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(NTB_URL, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", {"class": "table table-striped"})
    if not table:
        raise RuntimeError("NTB: FX table not found")

    tds = [td.get_text(strip=True).replace(",", "") for td in table.find_all("td")]
    if not tds:
        raise RuntimeError("NTB: no <td> found")

    # Detect tokens that look like currency codes (3–4 uppercase letters)
    pattern = re.compile(r"^[A-Z]{3,4}$")
    today = datetime.now(UTC).date().isoformat()
    rows = []

    buffer = []
    for token in tds:
        buffer.append(token)
        if pattern.match(token):
            # currency code reached → previous numeric values belong to it
            nums = [v for v in buffer[:-1] if re.match(r"^\d+(\.\d+)?$", v)]
            if len(nums) >= 2:
                buy_rate, sell_rate = float(nums[0]), float(nums[1])
                rows.append({
                    "date": today,
                    "bank": "Nations Trust Bank",
                    "currency_code": token,
                    "buy_rate": buy_rate,
                    "sell_rate": sell_rate
                })
            buffer.clear()

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("NTB: parsed no valid rows — table format changed again.")
    return df
