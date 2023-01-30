import logging
import sys

from sqlalchemy import Column, DateTime, MetaData, Numeric, String, Table, create_engine
from sqlalchemy.orm import mapper
from ticker import config
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
    if hasattr(sys, "_called_from_test"):
        # called from within a test run
        pass
    else:
        # called "normally"
        engine = create_engine(config.get_mysql_uri(), isolation_level="SERIALIZABLE")
        metadata.create_all(engine)
    mapper(model.DailyPrice, daily_price)
