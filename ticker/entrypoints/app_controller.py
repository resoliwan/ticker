import logging

import arrow
from fastapi import FastAPI
from ticker import bootstrap, config, views
from ticker.domain import commands

logger = logging.getLogger(__name__)
bus, dep = bootstrap.bootstrap()

app = FastAPI()


@app.get("/tk/version/v1")
def get_version():
    return {"success": True, "version": "0.0.0"}


@app.post("/tk/daily/price/v1")
def create_daily_price(symbol: str, interval: int, a_range: int):
    try:
        cmd = commands.CreateDailyPrice(symbol, interval, a_range)
        bus.handle(cmd)
    except Exception as ex:
        return {"success": False, "message": str(ex)}

    return {"success": True}


@app.get("/tk/recent/daily/price/v1")
def get_recent_daily_price(symbol: str, a_range: int):
    res = views.get_recent_daily_prices(symbol, 5, bus.uow)
    if not res:
        return {"success": False}
    return res
