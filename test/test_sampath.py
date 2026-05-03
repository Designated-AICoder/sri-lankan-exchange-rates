# test/test_sampath.py
import pytest
from scrapers.sampath import fetch_sampath_bank_rates

def test_fetch_sampath_rates_basic():
    df = fetch_sampath_bank_rates()
    assert not df.empty
    assert (df["bank"] == "Sampath Bank").all()
    assert "USD" in df["currency_code"].values
    assert df["buy_rate"].dtype in [float, 'float64']
    assert df["sell_rate"].dtype in [float, 'float64']
