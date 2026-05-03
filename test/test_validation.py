# test/test_validation.py
import pytest
from utils.validation import validate_scraped_data

def test_validation_engine_catches_bad_data():
    bad_data = [
        # Valid entry
        {"date": "2026-05-03", "bank": "Test Bank", "currency_code": "USD", "buy_rate": 300.0, "sell_rate": 310.0},
        # Invalid: Negative rate
        {"date": "2026-05-03", "bank": "Test Bank", "currency_code": "USD", "buy_rate": -10.0, "sell_rate": 310.0},
        # Invalid: Too high rate (sanity check)
        {"date": "2026-05-03", "bank": "Test Bank", "currency_code": "USD", "buy_rate": 20000.0, "sell_rate": 310.0},
        # Invalid: Missing currency code
        {"date": "2026-05-03", "bank": "Test Bank", "currency_code": "", "buy_rate": 300.0, "sell_rate": 310.0},
    ]
    
    valid_df, invalid_records = validate_scraped_data(bad_data)
    
    assert len(valid_df) == 1
    assert len(invalid_records) == 3
    assert "buy_rate" in invalid_records[0]
    assert "validation_error" in invalid_records[0]
