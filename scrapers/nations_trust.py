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

    # Detect tokens that look like currency codes (3 uppercase letters)
    pattern = re.compile(r"^[A-Z]{3}$")
    today = datetime.now(UTC).date().isoformat()
    rows = []

    current_currency = None
    nums_buffer = []

    for token in tds:
        if pattern.match(token):
            # If we already have a currency in progress, save it
            if current_currency and len(nums_buffer) >= 2:
                rows.append({
                    "date": today,
                    "bank": "Nations Trust Bank",
                    "currency_code": current_currency,
                    "buy_rate": float(nums_buffer[0]),
                    "sell_rate": float(nums_buffer[1])
                })
            
            # Start new currency
            current_currency = token
            nums_buffer = []
        else:
            # If it's a number, add to buffer
            if re.match(r"^\d+(\.\d+)?$", token):
                nums_buffer.append(token)

    # Don't forget the last currency
    if current_currency and len(nums_buffer) >= 2:
        rows.append({
            "date": today,
            "bank": "Nations Trust Bank",
            "currency_code": current_currency,
            "buy_rate": float(nums_buffer[0]),
            "sell_rate": float(nums_buffer[1])
        })

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("NTB: parsed no valid rows — table format changed.")
    return df
