from __future__ import annotations

# import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

import pandas as pd

# from typing import Dict

# import arrow


@dataclass
class DailyPrice:
    as_of_date: datetime
    symbol: str
    high: Decimal
    low: Decimal
    open: Decimal
    close: Decimal
    volume: Decimal

    @staticmethod
    def create_from_price(price: pd.Series) -> DailyPrice:
        return DailyPrice(
            **{
                "as_of_date": price["Date"],
                "symbol": price["Symbol"],
                "high": price["High"],
                "low": price["Low"],
                "open": price["Open"],
                "close": price["Close"],
                "volume": price["Volume"],
            }
        )
