import os
import pandas as pd
from scrapers.nations_trust import fetch_nations_trust_rates
from utils.normalization import normalize_currency_aliases

DATA_DIR = "data"
MASTER_CSV = os.path.join(DATA_DIR, "fxrates_master.csv")

def run_all_scrapers():
    df_ntb = None
    print("Running Nations Trust Bank scraper...")
    df_ntb = fetch_nations_trust_rates()
    df_ntb = normalize_currency_aliases(df_ntb)
    print(f"✅ Nations Trust Bank: {len(df_ntb)} rows scraped.")
    return df_ntb

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        df_new = run_all_scrapers()
    except Exception as e:
        print(f"❌ Scraper failed: {e}")
        exit(1)

    if os.path.exists(MASTER_CSV):
        df_old = pd.read_csv(MASTER_CSV, dtype={"currency_code": str})
        df = pd.concat([df_old, df_new], ignore_index=True)
        df.drop_duplicates(subset=["date", "bank", "currency_code"], keep="last", inplace=True)
    else:
        df = df_new

    df.to_csv(MASTER_CSV, index=False)
    print(f"✅ Data saved to {MASTER_CSV}. Total rows: {len(df)}")
