import abc
import logging
from typing import Dict

import arrow
import pandas as pd
import requests
import yfinance as yf
from arrow import Arrow
from ticker import config

yf.pdr_override()

logger = logging.getLogger(__name__)


class AbstractVendorProxy(abc.ABC):
    @abc.abstractmethod
    def get_daily_prices(
        self, symbol: str, interval: int, a_range: int
    ) -> pd.DataFrame:
        raise NotImplementedError


class HttpYahooProxy(AbstractVendorProxy):
    def get_daily_prices_by_json(
        self, symbol: str, interval: int, a_range: int
    ) -> dict:
        url = config.get_yahoo_api_url()
        # https://query1.finance.yahoo.com/v8/finance/chart/005930.KS?interval=1d&range=5d
        # https://query1.finance.yahoo.com/v8/finance/chart/005930.KS?interval=1d&range=5d
        params = {
            "interval": f"{interval}d",
            "range": f"{a_range}d",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        try:
            res = requests.get(f"{url}/{symbol}", params=params, headers=headers)
            res.raise_for_status()
        except Exception as ex:
            logger.error(f"{ex}, {params}")
            raise

        return res.json()

    def get_daily_prices(
        self, symbol: str, interval: int, a_range: int
    ) -> pd.DataFrame:
        res = self.get_daily_prices_by_json(symbol, interval, a_range)
        result = res["chart"]["result"][0]
        quote = result["indicators"]["quote"][0]
        timestamp = result["timestamp"]
        open = quote["open"]
        high = quote["high"]
        low = quote["low"]
        close = quote["close"]
        volume = quote["volume"]

        return pd.DataFrame(
            data={
                "Symbol": symbol,
                "Date": timestamp,
                "Open": open,
                "High": high,
                "Low": low,
                "Close": close,
                "Volume": volume,
            }
        )


class YFianceProxy(AbstractVendorProxy):
    def get_daily_prices(
        self, symbol: str, interval: int, a_range: int
    ) -> pd.DataFrame:
        if interval != 1:
            raise Exception("interval should be 1")
        df = yf.download(
            symbol,
            start=arrow.utcnow().shift(days=-1 * a_range).datetime,
            end=arrow.utcnow().datetime,
        )
        df = df.reset_index()
        df["Symbol"] = symbol
        return df
