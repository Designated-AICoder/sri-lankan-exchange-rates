# scrapers/amana.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, UTC

AMANA_BANK_URL = "https://www.amanabank.lk/business/treasury/exchange-rates.html"

def fetch_amana_bank_rates() -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(AMANA_BANK_URL, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")
    if not table:
        raise RuntimeError("Amana Bank: FX table not found")

    rows = []
    today = datetime.now(UTC).date().isoformat()
    
    # 0: Currency Name
    # 1: Bank Buying
    # 2: Bank Selling
    for tr in table.find_all("tr"):
        tds = tr.find_all(["td", "th"])
        if len(tds) < 3:
            continue
            
        currency_name = tds[0].get_text(strip=True).upper()
        if "CURRENCY" in currency_name or not currency_name or "EXCHANGE RATES" in currency_name:
            continue
            
        try:
            buy_val = tds[1].get_text(strip=True).replace(",", "")
            sell_val = tds[2].get_text(strip=True).replace(",", "")
            
            buy_rate = float(buy_val) if buy_val and buy_val != "-" else 0.0
            sell_rate = float(sell_val) if sell_val and sell_val != "-" else 0.0
            
            if buy_rate > 0 or sell_rate > 0:
                rows.append({
                    "date": today,
                    "bank": "Amana Bank",
                    "currency_code": currency_name,
                    "buy_rate": buy_rate,
                    "sell_rate": sell_rate
                })
        except (ValueError, IndexError):
            continue

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("Amana Bank: No valid rows parsed.")
    
    return df
