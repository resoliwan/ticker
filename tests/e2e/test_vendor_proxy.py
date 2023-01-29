import datetime

from ticker.adapters.vendor_proxy import HttpYahooProxy, MockVendorProxy, YFianceProxy


def test_http_get_prices_by_json():
    yahoo_proxy = HttpYahooProxy()

    res = yahoo_proxy.get_daily_prices_by_json("005930.KS", 1, 5)
    assert res.get("success", True), res


def test_time_format():
    import pytz

    tz = pytz.timezone("Asia/Seoul")
    print(datetime.datetime.fromtimestamp(1674086400, tz))
    print(datetime.datetime.fromtimestamp(1674086400))


def test_http_get_prices_by_df():
    yahoo_proxy = HttpYahooProxy()

    df = yahoo_proxy.get_daily_prices("005930.KS", 1, 5)
    # print(df)
    # assert False
    #                        Date     Symbol     Open  ...      Low    Close    Volume
    # 0 2023-01-19 09:00:00+09:00  005930.KS  60500.0  ...  60400.0  61500.0  12808490
    # 1 2023-01-20 09:00:00+09:00  005930.KS  62100.0  ...  61100.0  61800.0   9646327
    # 2 2023-01-25 09:00:00+09:00  005930.KS  63500.0  ...  63000.0  63300.0     39217
    # 3 2023-01-26 09:00:00+09:00  005930.KS  63800.0  ...  63300.0  63800.0     54188
    # 4 2023-01-27 09:00:00+09:00  005930.KS  64400.0  ...  63900.0  64600.0     44282
    assert df["Symbol"][0] == "005930.KS"


def test_pdr_get_prices_by_df():
    yahoo_proxy = YFianceProxy()

    df = yahoo_proxy.get_daily_prices("005930.KS", 1, 5)
    # print(df)
    # assert False
    #                     Date     Open     High  ...  Adj Close    Volume     Symbol
    # 0 2023-01-19 00:00:00+09:00  60500.0  61500.0  ...    61500.0  12808490  005930.KS
    # 1 2023-01-20 00:00:00+09:00  62100.0  62300.0  ...    61800.0   9646327  005930.KS
    # 2 2023-01-25 00:00:00+09:00  63500.0  63700.0  ...    63300.0     39217  005930.KS
    # 3 2023-01-26 00:00:00+09:00  63800.0  63900.0  ...    63800.0     54188  005930.KS
    # 4 2023-01-27 00:00:00+09:00  64400.0  65000.0  ...    64600.0     44282  005930.KS
    assert df["Symbol"][0] == "005930.KS"


def test_mock_get_prices_by_df():
    yahoo_proxy = MockVendorProxy()

    df = yahoo_proxy.get_daily_prices("005930.KS", 1, 5)
    # print(df)
    # assert False
    assert df["Symbol"][0] == "005930.KS"
