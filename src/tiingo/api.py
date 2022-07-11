from os import getenv
from datetime import datetime, timedelta
import pandas as pd
import requests


class API(object):
    def __init__(self, key: str):
        self.key = key
        self.headers = {'Content-Type': 'application/json'}

    @classmethod
    def from_env(cls):
        key = getenv("TIINGO_KEY")
        assert key, "Must set environment variable 'TIINGO_KEY'"
        return cls(key=key)

    def _get(self, url: str, **kwargs) -> dict:
        """
        -----------
        Submit a GET request to Tiingo API
        -----------
        [params]
            'url' -> url to submit request to
            **'kwargs' -> params to submit to api endpoint
        """
        kwargs.update({"token": self.key})
        r = requests.get(url, params=kwargs, headers=self.headers)
        assert r.ok, r.text
        return r.json()


class EOD(API):
    """
    ---------
    Tiingo End of Day Data API Wrapper
    ---------
    [docs]
        https://api.tiingo.com/documentation/end-of-day
    """
    def __init__(self, key: str):
        super().__init__(key=key)
        self.url = "https://api.tiingo.com/tiingo/daily/"
        self.meta_endpoint = "{ticker}"
        self.price_endpoint = "{ticker}/prices"

    def get_meta(self, ticker: str) -> dict:
        """
        ---------
        Returns ticker metadata
        ---------
        [params]
            'ticker' -> ticker to query
        [returns]
            a dict with the following keys:
                1. ticker
                2. name
                3. exchangeCode
                4. description
                5. startDate
                6. endDate
        ---------
        """
        url = self.url + self.meta_endpoint.format(ticker=ticker)
        return self._get(url)

    def get_prices(self, 
                   ticker: str, 
                   start_date: str = None, 
                   end_date: str = None, 
                   resample_freq: str = None) -> pd.DataFrame:
        """
        ---------
        Returns price data
        ---------
        [params]
            'ticker' -> ticker to query for
            'start_date' -> yyyy-mm-dd; str; optional
            'end_date -> yyyy-mm-dd; str; optional
            'resample_freq' - interval at which to sample data; optional
                [allowed values]
                    - 'daily', 'weekly', 'monthly', or 'annually'
        
        [note]
            if no keyword arguments passed except for ticker, then Tiingo will
            return only the latest price
        ---------
        """
        url = self.url + self.price_endpoint.format(ticker=ticker)
        data = self._get(url=url, startDate=start_date, endDate=end_date, resampleFreq=resample_freq)
        return pd.DataFrame(data)


class IEX(API):
    """
    ---------
    Tiingo IEX Data API Wrapper
    ---------
    [docs]
        https://api.tiingo.com/documentation/iex
    """
    def __init__(self, key: str):
        super().__init__(key=key)
        self.url = "https://api.tiingo.com/iex/" # will return top of book for all tickers
        self.top_endpoint = "{ticker}"
        self.price_endpoint = "{ticker}/prices"
    
    def get_top(self, ticker: str, as_pandas: bool = False) -> pd.DataFrame:
        url = self.url + self.top_endpoint.format(ticker=ticker)
        data = self._get(url=url)
        return pd.DataFrame(data) if as_pandas else data
    
    def get_prices(self, 
                   ticker: str, 
                   start_date: str, 
                   end_date: str=None, 
                   resample_freq: str = "5min") -> pd.DataFrame:
        """
        ---------
        Returns price data
        ---------
        [params]
            'ticker' -> ticker to query for
            'start_date' -> yyyy-mm-dd; str
            'end_date -> yyyy-mm-dd; str
            'resample_freq' - interval at which to sample data; default 5min
                [allowed values]
                    - 'Xmin', or 'Xhour'
        [note]
            if no keyword arguments passed except for ticker, then Tiingo will
            return only the latest prices
        ---------
        """
        url = self.url + self.price_endpoint.format(ticker=ticker)
        if not end_date:
            curr_start = datetime.today()
        else:
            curr_start = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        data = []
        while curr_start > start_date + timedelta(1):
            batch = self._get(url=url, startDate=start_date, endDate=curr_start, resampleFreq=resample_freq)
            df_start = pd.to_datetime(batch[0]["date"]).to_pydatetime().replace(tzinfo=None)
            if curr_start == df_start: # means the api doesn't provide data this early
                break
            data = batch + data
            curr_start = df_start
        data = pd.DataFrame(data)
        data.drop_duplicates(subset=["date"], inplace=True)
        return data.reset_index(drop=True)


class Crypto(API):
    """
    ---------
    Tiingo Crypto API Wrapper
    ---------
    [docs]
        https://api.tiingo.com/documentation/crypto
    """
    def __init__(self, key: str):
        super().__init__(key=key)
        self.url = "https://api.tiingo.com/tiingo/crypto/" # will return top of book for all tickers
        self.top_endpoint = "top/"
        self.price_endpoint = "prices/"

    def get_top(self, ticker: str) -> list[dict]:
        url = self.url + self.top_endpoint
        data = self._get(url=url, tickers=ticker)
        return data

    def get_meta(self, ticker: str) -> list[dict]:
        return self._get(self.url, tickers=ticker)
    
    def get_prices(self, 
                   ticker: str, 
                   start_date: str = None, 
                   end_date: str = None, 
                   resample_freq: str = "5min") -> pd.DataFrame:
        """
        ---------
        Returns price data
        ---------
        [params]
            'ticker' -> ticker to query for
            'start_date' -> yyyy-mm-dd; str
            'end_date -> yyyy-mm-dd; str
            'resample_freq' - interval at which to sample data; default 5min
                [allowed values]
                    - 'Xmin', or 'Xhour'
        [note]
            if no keyword arguments passed except for ticker, then Tiingo will
            return only the latest prices
        ---------
        """
        def get_batch(**kwargs):
            data = self._get(**kwargs)
            if data:
                data = data[0].get("priceData")
            return data

        url = self.url + self.price_endpoint
        data = get_batch(url=url, startDate=start_date, endDate=end_date, resampleFreq=resample_freq, tickers=ticker)
        if not data:
            return pd.DataFrame()

        curr_end = pd.to_datetime(data[-1]["date"]).to_pydatetime().replace(tzinfo=None)
        if not end_date:
            end_date = datetime.today()
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        while curr_end < end_date:
            batch = get_batch(url=url, startDate=curr_end, endDate=end_date, resampleFreq=resample_freq, tickers=ticker)
            curr_end = pd.to_datetime(batch[-1]["date"]).to_pydatetime().replace(tzinfo=None)
            last_end = pd.to_datetime(data[-1]["date"]).to_pydatetime().replace(tzinfo=None)
            if last_end == curr_end:
                break
            data += batch
        data = pd.DataFrame(data)
        data.drop_duplicates(subset=["date"], inplace=True)
        return data.reset_index(drop=True)
