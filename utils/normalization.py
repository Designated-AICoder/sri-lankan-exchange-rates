# utils/normalization.py

import pandas as pd

CURRENCY_ALIASES = {
    "US DOLLAR": "USD",
    "US DOLLARS": "USD",
    "USD": "USD",
    "EURO": "EUR",
    "STERLING POUND": "GBP",
    "STERLING POUNDS": "GBP",
    "GBP": "GBP",
    "JAPANESE YEN": "JPY",
    "JPY": "JPY",
    "SINGAPORE DOLLARS": "SGD",
    "SGD": "SGD",
    "AUSTRALIAN DOLLARS": "AUD",
    "AUD": "AUD",
    "SWISS FRANCS": "CHF",
    "CHF": "CHF",
    "KUWAITI DINARS": "KWD",
    "KWD": "KWD",
    "OMANI RIYALS": "OMR",
    "OMR": "OMR",
    "SAUDI ARABIAN RIYALS": "SAR",
    "SAR": "SAR",
    "UAE DIRHAMS": "AED",
    "AED": "AED",
    "QATAR RIYALS": "QAR",
    "QAR": "QAR",
    "JORDANIAN DINARS": "JOD",
    "JOD": "JOD",
    "BAHRAIN DINARS": "BHD",
    "BHD": "BHD",
    "INDIAN RUPEES": "INR",
    "INR": "INR",
    "CANADIAN DOLLAR": "CAD",
    "CAD": "CAD",
    "NEW ZEALAND DOLLARS": "NZD",
    "NZD": "NZD"
}

def normalize_currency_aliases(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "currency_code" not in df.columns:
        raise ValueError("Normalization: expected column 'currency_code'")

    df["currency_code"] = df["currency_code"].map(
        lambda x: CURRENCY_ALIASES.get(x.strip().upper(), x.strip().upper())
    )

    unmapped = df.loc[~df["currency_code"].isin(CURRENCY_ALIASES.values()), "currency_code"].unique()
    if len(unmapped):
        print("⚠️ WARNING: Unrecognized currency codes:", unmapped.tolist())

    return df
