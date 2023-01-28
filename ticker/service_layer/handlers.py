# pylint: disable=unused-argument
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict, List, Type

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
        print(uow)
        for _, row in df.iterrows():
            print(row)
            print(model.DailyPrice.create_from_price(row))
            uow.price.add(item=model.DailyPrice.create_from_price(row))
        uow.commit()


EVENT_HANDLERS = {}
COMMAND_HANDLERS = {
    commands.CreateDailyPrice: create_daily_prices,
}
