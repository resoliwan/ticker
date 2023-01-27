import logging

from sqlalchemy import Column, DateTime, MetaData, Numeric, String, Table
from sqlalchemy.orm import mapper
from ticker.domain import model

logger = logging.getLogger(__name__)

metadata = MetaData()

daily_price = Table(
    "daily_price",
    metadata,
    Column("as_of_date", DateTime, primary_key=True),
    Column("symbol", String(255), primary_key=True),
    Column("high", Numeric(15, 3), default=0),
    Column("low", Numeric(15, 3), default=0),
    Column("open", Numeric(15, 3), default=0),
    Column("close", Numeric(15, 3), default=0),
    Column("volume", Numeric(15, 3), default=0),
)


def start_mappers():
    logger.info("Starting mappers")
    mapper(model.DailyPrice, daily_price)
