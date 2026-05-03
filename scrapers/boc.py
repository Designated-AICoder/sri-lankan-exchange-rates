# scrapers/boc.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, UTC
import re

BOC_URL = "https://www.boc.lk/rates-tariff"

def fetch_boc_rates() -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(BOC_URL, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    # BOC table is usually inside a div with class 'table-responsive' or just the first table in the section
    table = soup.find("table")
    if not table:
        raise RuntimeError("BOC: FX table not found")

    rows = []
    today = datetime.now(UTC).date().isoformat()
    
    # Skip the header rows (BOC has multiple header rows)
    # We look for rows that have at least 7 columns
    for tr in table.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 7:
            continue
            
        currency_code = tds[0].get_text(strip=True).upper()
        # Skip header-like rows that might have escaped the skip
        if not re.match(r"^[A-Z]{3}$", currency_code):
            continue
            
        try:
            # We use TT rates (Column 5 and 6) to stay consistent with NTB
            buy_val = tds[5].get_text(strip=True).replace(",", "")
            sell_val = tds[6].get_text(strip=True).replace(",", "")
            
            # Handle '-' or empty strings
            buy_rate = float(buy_val) if buy_val and buy_val != "-" else 0.0
            sell_rate = float(sell_val) if sell_val and sell_val != "-" else 0.0
            
            if buy_rate > 0 or sell_rate > 0:
                rows.append({
                    "date": today,
                    "bank": "Bank of Ceylon",
                    "currency_code": currency_code,
                    "buy_rate": buy_rate,
                    "sell_rate": sell_rate
                })
        except (ValueError, IndexError):
            continue

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("BOC: parsed no valid rows. Website structure might have changed.")
    
    return df
