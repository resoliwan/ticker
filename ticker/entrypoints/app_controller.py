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


# @app.get("/tk/ticker/v1")
# def get_ticker(symbol, interval, range):
#     try:
#         cmd = commands.CreateDailyPrice(symbol, interval, range)
#         bus.handle(cmd)
#     except Exception as ex:
#         return {"success": False, "message": str(ex)}
#
#     return True


@app.post("/tk/daily/price/v1")
def create_daily_price(symbol: str, interval: int, range: int):
    try:
        cmd = commands.CreateDailyPrice(symbol, interval, range)
        bus.handle(cmd)
    except Exception as ex:
        return {"success": False, "message": str(ex)}

    return {"success": True}
