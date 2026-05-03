# test/test_nations_trust.py
import pytest
from scrapers.nations_trust import fetch_nations_trust_rates

def test_fetch_nations_trust_rates_basic():
    df = fetch_nations_trust_rates()
    # Basic shape tests
    assert not df.empty
    assert set(["date", "bank", "currency_code", "buy_rate", "sell_rate"]).issubset(df.columns)
    # Check some typical currency
    assert "USD" in df["currency_code"].values
    assert df["buy_rate"].dtype == float or df["buy_rate"].dtype == "float64"
    assert df["sell_rate"].dtype == float or df["sell_rate"].dtype == "float64"
