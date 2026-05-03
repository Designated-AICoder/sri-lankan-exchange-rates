# scrapers/sampath.py
import requests
import pandas as pd
from datetime import datetime, UTC

SAMPATH_API_URL = "https://www.sampath.lk/api/exchange-rates"

def fetch_sampath_bank_rates() -> pd.DataFrame:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    resp = requests.get(SAMPATH_API_URL, headers=headers, timeout=30)
    resp.raise_for_status()

    json_data = resp.json()
    if not json_data.get("success") or "data" not in json_data:
        raise RuntimeError(f"Sampath API Error: {json_data.get('description', 'Unknown error')}")

    today = datetime.now(UTC).date().isoformat()
    rows = []

    for item in json_data["data"]:
        try:
            code = item.get("CurrCode", "").strip().upper()
            if not code or len(code) != 3:
                continue

            buy_rate = float(item.get("TTBUY", 0))
            sell_rate = float(item.get("TTSEL", 0))

            if buy_rate > 0 or sell_rate > 0:
                rows.append({
                    "date": today,
                    "bank": "Sampath Bank",
                    "currency_code": code,
                    "buy_rate": buy_rate,
                    "sell_rate": sell_rate
                })
        except (ValueError, TypeError):
            continue

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("Sampath API: No valid rates found in response.")
    
    return df
