# pylint: disable=no-self-use
from __future__ import annotations

import arrow
import pytest
from ticker.domain import commands, events, model

pytestmark = pytest.mark.usefixtures("mappers")


def test_create_daily_price(bootstrap_test_app):
    bus, _ = bootstrap_test_app
    bus.handle(
        commands.CreateDailyPrice(
            **{
                "symbol": "005930.KS",
                "interval": 1,
                "a_range": 5,
            }
        )
    )
