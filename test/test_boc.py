# test/test_boc.py
import pytest
from scrapers.boc import fetch_boc_rates

def test_fetch_boc_rates_basic():
    df = fetch_boc_rates()
    
    # Basic structure checks
    assert not df.empty, "DataFrame should not be empty"
    expected_cols = ["date", "bank", "currency_code", "buy_rate", "sell_rate"]
    assert all(col in df.columns for col in expected_cols), f"Missing columns in {df.columns}"
    
    # Check for Bank of Ceylon identity
    assert (df["bank"] == "Bank of Ceylon").all()
    
    # Check for common currencies
    currencies = df["currency_code"].tolist()
    assert "USD" in currencies, "USD should be in BOC rates"
    assert "GBP" in currencies or "EUR" in currencies, "Major currencies should be present"
    
    # Check data types and values
    assert df["buy_rate"].dtype in [float, 'float64']
    assert df["sell_rate"].dtype in [float, 'float64']
    
    # Check that rates are reasonable (e.g., > 100 LKR for USD/GBP)
    usd_buy = df.loc[df["currency_code"] == "USD", "buy_rate"].iloc[0]
    assert usd_buy > 200, f"USD rate {usd_buy} seems too low for LKR"
