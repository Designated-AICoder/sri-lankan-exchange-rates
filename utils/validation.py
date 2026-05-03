# utils/validation.py
from typing import List, Dict, Any, Tuple
from utils.models import FXRate
import pandas as pd

def validate_scraped_data(data: List[Dict[str, Any]]) -> Tuple[pd.DataFrame, List[Dict[str, Any]]]:
    """
    Validates a list of scraped dictionaries against the FXRate model.
    Returns a tuple of (valid_df, invalid_records).
    """
    valid_records = []
    invalid_records = []

    for entry in data:
        try:
            # Pydantic validation
            rate = FXRate(**entry)
            valid_records.append(rate.model_dump())
        except Exception as e:
            # Capture what went wrong and which entry failed
            entry['validation_error'] = str(e)
            invalid_records.append(entry)

    df = pd.DataFrame(valid_records)
    return df, invalid_records
