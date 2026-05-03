# test/test_commercial.py
import pytest
from scrapers.commercial import fetch_commercial_bank_rates

def test_fetch_commercial_rates_basic():
    df = fetch_commercial_bank_rates()
    
    assert not df.empty, "DataFrame should not be empty"
    assert (df["bank"] == "Commercial Bank").all()
    # Check for normalized USD code (the scraper should return 'US DOLLARS' 
    # which normalization will turn into 'USD' in main.py, 
    # but the raw scraper result might still be 'US DOLLARS' depending on where we check)
    # Actually, in run_all_scrapers, we call normalize_currency_aliases(df)
    
    # Check data types
    assert df["buy_rate"].dtype in [float, 'float64']
    assert df["sell_rate"].dtype in [float, 'float64']
    
    # At least some major currencies should be there
    codes = df["currency_code"].tolist()
    assert any("DOLLAR" in c or "USD" in c for c in codes)
