from ticker.adapters.vendor_proxy import HttpYahooProxy, MockVendorProxy, YFianceProxy


def test_http_get_prices_by_json():
    yahoo_proxy = HttpYahooProxy()

    res = yahoo_proxy.get_daily_prices_by_json("005930.KS", 1, 5)
    assert res.get("success", True), res


def test_http_get_prices_by_df():
    yahoo_proxy = HttpYahooProxy()

    df = yahoo_proxy.get_daily_prices("005930.KS", 1, 5)
    assert df["symbol"][0] == "005930.KS"


def test_pdr_get_prices_by_df():
    yahoo_proxy = YFianceProxy()

    df = yahoo_proxy.get_daily_prices("005930.KS", 1, 5)
    print(df)
    assert df["Symbol"][0] == "005930.KS"


def test_mock_get_prices_by_df():
    yahoo_proxy = MockVendorProxy()

    df = yahoo_proxy.get_daily_prices("005930.KS", 1, 5)
    print(df)
    assert df["Symbol"][0] == "005930.KS"
