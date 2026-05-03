# scrapers/commercial.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, UTC
import re

COMMERCIAL_URL = "https://www.combank.lk/rates-tariff#exchange-rates"

def fetch_commercial_bank_rates() -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(COMMERCIAL_URL, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    # Commercial Bank's table is usually in the #exchange-rates section
    container = soup.find("div", {"id": "exchange-rates"})
    if not container:
        # Fallback to searching all tables
        tables = soup.find_all("table")
        for t in tables:
            if "US DOLLAR" in t.get_text().upper():
                table = t
                break
        else:
            raise RuntimeError("Commercial Bank: FX table not found")
    else:
        table = container.find("table")

    rows = []
    today = datetime.now(UTC).date().isoformat()
    
    # Standard columns based on browser analysis:
    # 0: Currency Name
    # 5: TT Buying
    # 6: TT Selling
    for tr in table.find_all("tr"):
        tds = tr.find_all(["td", "th"])
        if len(tds) < 7:
            continue
            
        currency_name = tds[0].get_text(strip=True).upper()
        # Skip header rows
        if "CURRENCY" in currency_name or "BUYING" in currency_name:
            continue
            
        try:
            buy_val = tds[5].get_text(strip=True).replace(",", "")
            sell_val = tds[6].get_text(strip=True).replace(",", "")
            
            # Handle '-' or empty
            buy_rate = float(buy_val) if buy_val and buy_val != "-" else 0.0
            sell_rate = float(sell_val) if sell_val and sell_val != "-" else 0.0
            
            if buy_rate > 0 or sell_rate > 0:
                rows.append({
                    "date": today,
                    "bank": "Commercial Bank",
                    "currency_code": currency_name, # Normalization utility will handle "US DOLLARS" -> "USD"
                    "buy_rate": buy_rate,
                    "sell_rate": sell_rate
                })
        except (ValueError, IndexError):
            continue

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("Commercial Bank: No valid rows parsed.")
    
    return df
