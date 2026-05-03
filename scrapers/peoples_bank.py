# scrapers/peoples_bank.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, UTC
import re

PEOPLES_BANK_URL = "https://www.peoplesbank.lk/exchange-rates/"

def fetch_peoples_bank_rates() -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(PEOPLES_BANK_URL, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")
    if not table:
        raise RuntimeError("People's Bank: FX table not found")

    rows = []
    today = datetime.now(UTC).date().isoformat()
    
    # 0: Currency Name
    # 5: TT Buying
    # 6: TT Selling
    for tr in table.find_all("tr"):
        tds = tr.find_all(["td", "th"])
        if len(tds) < 7:
            continue
            
        currency_name = tds[0].get_text(strip=True).upper()
        if "CURRENCY" in currency_name or not currency_name:
            continue
            
        try:
            # Clean numeric strings
            buy_val = tds[5].get_text(strip=True).replace(",", "")
            sell_val = tds[6].get_text(strip=True).replace(",", "")
            
            buy_rate = float(buy_val) if buy_val and buy_val != "-" else 0.0
            sell_rate = float(sell_val) if sell_val and sell_val != "-" else 0.0
            
            if buy_rate > 0 or sell_rate > 0:
                rows.append({
                    "date": today,
                    "bank": "People's Bank",
                    "currency_code": currency_name,
                    "buy_rate": buy_rate,
                    "sell_rate": sell_rate
                })
        except (ValueError, IndexError):
            continue

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("People's Bank: No valid rows parsed.")
    
    return df
