import pandas as pd
import os

MASTER_CSV = "data/fxrates_master.csv"

if os.path.exists(MASTER_CSV):
    # Read the CSV
    df = pd.read_csv(MASTER_CSV)
    
    # We only care about these columns
    target_cols = ["date", "bank", "currency_code", "buy_rate", "sell_rate"]
    
    # Filter for rows that have at least some valid data in the target columns
    # and drop the junk columns (US Dollar, Euro, etc.)
    df_clean = df[target_cols].copy()
    
    # Drop rows where 'bank' is NaN (this will remove the malformed 2025-10-19 row)
    df_clean.dropna(subset=["bank"], inplace=True)
    
    # Save back to CSV
    df_clean.to_csv(MASTER_CSV, index=False)
    print(f"✅ Cleaned {MASTER_CSV}. Kept columns: {target_cols}")
else:
    print("❌ CSV not found.")
