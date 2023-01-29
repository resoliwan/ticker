import logging

from ticker.service_layer import unit_of_work

logger = logging.getLogger(__name__)


def get_recent_daily_prices(
    symbol: str, a_range: int, uow: unit_of_work.SqlAlchemyUnitOfWork
):
    with uow:
        result = uow.session.execute(
            """
            SELECT
                *
            FROM
                daily_price
            WHERE symbol = :symbol
            ORDER BY as_of_date DESC
            LIMIT :a_range 
            """,
            dict(symbol=symbol, a_range=a_range),
        )

    return [dict(row) for row in result.fetchall()]
