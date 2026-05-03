import os
import pandas as pd
from scrapers.nations_trust import fetch_nations_trust_rates
from scrapers.boc import fetch_boc_rates
from utils.normalization import normalize_currency_aliases

DATA_DIR = "data"
MASTER_CSV = os.path.join(DATA_DIR, "fxrates_master.csv")

def run_all_scrapers():
    all_dfs = []
    
    # List of scrapers to run
    registry = [
        ("Nations Trust Bank", fetch_nations_trust_rates),
        ("Bank of Ceylon", fetch_boc_rates)
    ]
    
    for bank_name, scraper_func in registry:
        try:
            print(f"Running {bank_name} scraper...")
            df = scraper_func()
            df = normalize_currency_aliases(df)
            print(f"✅ {bank_name}: {len(df)} rows scraped.")
            all_dfs.append(df)
        except Exception as e:
            print(f"❌ {bank_name} failed: {e}")
            
    if not all_dfs:
        raise RuntimeError("All scrapers failed. No data to save.")
        
    return pd.concat(all_dfs, ignore_index=True)

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        df_new = run_all_scrapers()
    except Exception as e:
        print(f"❌ Global error: {e}")
        exit(1)

    if os.path.exists(MASTER_CSV):
        df_old = pd.read_csv(MASTER_CSV, dtype={"currency_code": str})
        df = pd.concat([df_old, df_new], ignore_index=True)
        df.drop_duplicates(subset=["date", "bank", "currency_code"], keep="last", inplace=True)
    else:
        df = df_new

    df.to_csv(MASTER_CSV, index=False)
    print(f"✅ Data saved to {MASTER_CSV}. Total rows: {len(df)}")
