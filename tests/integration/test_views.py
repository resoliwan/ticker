# pylint: disable=redefined-outer-name
from datetime import date
from decimal import Decimal
from unittest import mock

import arrow
import pytest
from sqlalchemy.orm import clear_mappers
from ticker import bootstrap, views
from ticker.domain import commands, model
from ticker.service_layer import unit_of_work

pytestmark = pytest.mark.usefixtures("mappers")
today = date.today()


def test_get_recent_daily_prices(bootstrap_test_app):
    bus, _ = bootstrap_test_app
    uow = bus.uow
    with uow:
        as_of_date = arrow.utcnow().datetime
        as_of_date = as_of_date.replace(tzinfo=None)
        p1 = model.DailyPrice(
            as_of_date,
            "TICKER1",
            Decimal(1),
            Decimal(2),
            Decimal(3),
            Decimal(4),
            Decimal(5),
        )
        bus.uow.price.add(p1)
        uow.commit()

    res = views.get_recent_daily_prices("TICKER1", 5, uow)
    # print(res)
    # assert False
    assert len(res) == 1
