# utils/models.py
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional

class FXRate(BaseModel):
    date: str # ISO format YYYY-MM-DD
    bank: str
    currency_code: str = Field(..., min_length=3, max_length=3)
    buy_rate: float = Field(..., gt=0)
    sell_rate: float = Field(..., gt=0)

    @field_validator('currency_code')
    @classmethod
    def must_be_uppercase(cls, v: str) -> str:
        return v.upper()

    @field_validator('buy_rate', 'sell_rate')
    @classmethod
    def check_sanity(cls, v: float) -> float:
        # Basic sanity check: No currency in SL is likely to be < 0.1 LKR 
        # and none should be > 10000 LKR for standard trading pairs
        if v < 0.01:
            raise ValueError(f"Rate {v} is suspiciously low.")
        if v > 15000:
            raise ValueError(f"Rate {v} is suspiciously high.")
        return v

class ScraperResult(BaseModel):
    bank: str
    rates: list[FXRate]
    status: str = "SUCCESS"
    error_message: Optional[str] = None
