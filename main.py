# main.py
import os
import pandas as pd
from loguru import logger
from scrapers.nations_trust import fetch_nations_trust_rates
from scrapers.boc import fetch_boc_rates
from scrapers.sampath import fetch_sampath_bank_rates
from scrapers.commercial import fetch_commercial_bank_rates
from scrapers.peoples_bank import fetch_peoples_bank_rates
from scrapers.amana import fetch_amana_bank_rates
from utils.normalization import normalize_currency_aliases
from utils.validation import validate_scraped_data

DATA_DIR = "data"
MASTER_CSV = os.path.join(DATA_DIR, "fxrates_master.csv")

# Setup logging
logger.add("logs/scraper_{time}.log", rotation="1 week", level="INFO")

def run_all_scrapers(dry_run=False):
    all_valid_dfs = []
    
    registry = [
        ("Nations Trust Bank", fetch_nations_trust_rates),
        ("Bank of Ceylon", fetch_boc_rates),
        ("Sampath Bank", fetch_sampath_bank_rates),
        ("Commercial Bank", fetch_commercial_bank_rates),
        ("People's Bank", fetch_peoples_bank_rates),
        ("Amana Bank", fetch_amana_bank_rates)
    ]
    
    for bank_name, scraper_func in registry:
        try:
            logger.info(f"Initiating {bank_name} scraper...")
            raw_df = scraper_func()
            normalized_df = normalize_currency_aliases(raw_df)
            
            # Validation Step (The "Shadow" Filter)
            valid_df, invalid_records = validate_scraped_data(normalized_df.to_dict('records'))
            
            if invalid_records:
                logger.warning(f"⚠️ {bank_name}: {len(invalid_records)} records failed validation!")
                for rec in invalid_records[:3]: # Log first few failures
                    logger.debug(f"Validation Failure Details: {rec}")

            if not valid_df.empty:
                logger.success(f"✅ {bank_name}: {len(valid_df)} valid records extracted.")
                all_valid_dfs.append(valid_df)
            else:
                logger.error(f"❌ {bank_name}: Zero valid records found after validation.")

        except Exception as e:
            logger.critical(f"💥 {bank_name} scraper crashed: {e}")
            
    if not all_valid_dfs:
        logger.error("System Failure: All scrapers failed validation.")
        return None
        
    return pd.concat(all_valid_dfs, ignore_index=True)

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    df_new = run_all_scrapers()
    
    if df_new is not None:
        if os.path.exists(MASTER_CSV):
            df_old = pd.read_csv(MASTER_CSV, dtype={"currency_code": str})
            df = pd.concat([df_old, df_new], ignore_index=True)
            df.drop_duplicates(subset=["date", "bank", "currency_code"], keep="last", inplace=True)
        else:
            df = df_new

        df.to_csv(MASTER_CSV, index=False)
        logger.info(f"Database Synchronized. Total dataset size: {len(df)} rows.")
    else:
        logger.warning("No data was saved this run due to validation failures.")
