from datetime import datetime
from decimal import Decimal

import arrow
import pytest
import ticker.adapters.repository as price_repo
from ticker.domain import model

pytestmark = pytest.mark.usefixtures("mappers")


def test_crud_portfolio_product(sqlite_session_factory):
    session = sqlite_session_factory()
    repo = price_repo.SqlAlchemyPriceRepository(session)

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
    p2 = model.DailyPrice(
        as_of_date,
        "TICKER2",
        Decimal(1),
        Decimal(2),
        Decimal(3),
        Decimal(4),
        Decimal(5),
    )
    repo.add(p1)
    repo.add(p2)
    assert repo.get_daily_price(p1.as_of_date, p1.symbol) == p1
    assert repo.get_daily_price(p2.as_of_date, p2.symbol) == p2


def test_get_recent_daily_prices(sqlite_session_factory):
    test_crud_portfolio_product(sqlite_session_factory)
    session = sqlite_session_factory()
    repo = price_repo.SqlAlchemyPriceRepository(session)

    res = repo.get_recent_daily_prices("TICKER1", 5)
    assert res
