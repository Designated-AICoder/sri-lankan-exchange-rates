# test/test_normalization.py

import pandas as pd
from utils.normalization import normalize_currency_aliases

def test_normalization_known_codes():
    df = pd.DataFrame({
        "currency_code": ["US DOLLARS", "euro", "INR"]
    })
    out = normalize_currency_aliases(df)
    assert "USD" in out["currency_code"].values
    assert "EUR" in out["currency_code"].values
    assert "INR" in out["currency_code"].values
