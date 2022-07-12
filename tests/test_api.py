from tiingo.api import EOD, IEX, Crypto


def test_eod():
    eod = EOD.from_env()
    spy_meta = eod.get_meta("spy")
    assert spy_meta["ticker"] == "spy"
    df = eod.get_prices(ticker="spy", start_date="2020-06-01", end_date="2021-06-01", resample_freq="daily")
    assert df.date.iloc[0][:10] == "2020-06-01"


def test_iex():
    iex = iex.from_env()
    spy_meta = iex.get_top("spy")
    assert isinstance(spy_meta, list) and len(spy_meta) == 1
    spy_meta = spy_meta[0]
    assert spy_meta.get("ticker") == "spy"
    # below will test extraction of historical data (loops until all data is queried)
    df = iex.get_prices(ticker="spy", start_date="2020-06-01", end_date="2022-06-01", resample_freq="15min")
    assert df.date.iloc[0][:10] == "2020-06-01"
    assert df.date.iloc[-1][:10] == "2022-06-01"


def test_crypto():
    c = Crypto.from_env()
    btc_meta = c.get_top("btcusd")
    assert isinstance(btc_meta, list) and len(btc_meta) == 1
    btc_meta = btc_meta[0]
    assert btc_meta.get("ticker") == "btcusd"
    # below will test extraction of historical data (loops until all data is queried)
    df = c.get_prices(ticker="btcusd", start_date="2020-06-01", end_date="2021-06-01", resample_freq="15min")
    assert df.date.iloc[0][:10] == "2020-06-01"
    assert df.date.iloc[-1][:10] == "2021-06-01"


def main():
    test_eod()
    test_iex()
    test_crypto()
