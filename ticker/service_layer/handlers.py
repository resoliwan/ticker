# pylint: disable=unused-argument
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict, List, Type

import pymysql
import sqlalchemy
from ticker.adapters.vendor_proxy import AbstractVendorProxy
from ticker.domain import commands, events, model

if TYPE_CHECKING:
    from ticker.service_layer import unit_of_work


def create_daily_prices(
    cmd: commands.CreateDailyPrice,
    vendor_proxy: AbstractVendorProxy,
    uow: unit_of_work.AbstractUnitOfWork,
):
    df = vendor_proxy.get_daily_prices(cmd.symbol, cmd.interval, cmd.a_range)
    with uow:
        try:
            for _, row in df.iterrows():
                uow.price.add(item=model.DailyPrice.create_from_price(row))
            uow.commit()
        except (sqlalchemy.exc.IntegrityError, pymysql.err.IntegrityError) as e:
            if e.orig.args[0] == 1062:
                # ignore duplicate key error
                pass
            else:
                raise e


EVENT_HANDLERS = {}
COMMAND_HANDLERS = {
    commands.CreateDailyPrice: create_daily_prices,
}
