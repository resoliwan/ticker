from __future__ import annotations

# import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

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
