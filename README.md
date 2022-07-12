# Tiingo-API Wrapper

## Usage

### End-of-Day Data

```
>>> from tiingo.api import EOD
>>> eod = EOD.from_env()
>>> eod.get_meta("spy")
{'ticker': 'SPY', 'name': 'S&P 500 ETF TRUST ETF', 'description': "Historical ETF prices for SPDR S&P 500 ETF (SPY). SPDR S&P 500 ETF Trust (the Trust) is an exchange traded fund. The Trust corresponds to the price and yield performance of the S&P 500 Index. The S&P 500 Index is composed of 500 selected stocks and spans over 24 separate industry groups. The Fund's investment sectors include information technology, financials, energy, health care, consumer staples, industrials, consumer discretionary, materials, utilities and telecommunication services.", 'startDate': '1993-01-29', 'endDate': '2022-07-11', 'exchangeCode': 'NYSE ARCA'}

>>> df = eod.get_prices(ticker="spy", start_date="2020-06-01", end_date="2021-06-01", resample_freq="weekly")
>>> df.head()
                       date    open    high     low   close     volume
0  2020-06-05T00:00:00.000Z  303.62  321.27  303.06  319.34  446855391
1  2020-06-12T00:00:00.000Z  320.22  323.41  298.60  304.21  647165283
2  2020-06-19T00:00:00.000Z  298.02  315.64  296.74  308.64  570398924
3  2020-06-26T00:00:00.000Z  307.99  314.50  299.42  300.05  490919328
4  2020-07-03T00:00:00.000Z  301.41  315.70  298.93  312.23  333726878
```

### IEX Data

```
>>> iex = IEX.from_env() 
>>> iex.get_top("spy")
[{'ticker': 'SPY', 'timestamp': '2022-07-11T20:00:00+00:00', 'lastSaleTimestamp': '2022-07-11T20:00:00+00:00', 'quoteTimestamp': '2022-07-11T20:00:00+00:00', 'open': 385.85, 'high': 386.87, 'low': 383.5, 'mid': None, 'tngoLast': 384.23, 'last': 384.23, 'lastSize': None, 'bidSize': None, 'bidPrice': None, 'askPrice': None, 'askSize': None, 'volume': 58366945, 'prevClose': 388.67}]

>>> df = iex.get_prices(ticker="spy", start_date="2020-06-01", end_date="2022-06-01", resample_freq="15min")
>>> df.head()
                       date    close     high      low     open
0  2020-06-01T13:30:00.000Z  304.200  304.285  303.040  303.640
1  2020-06-01T13:45:00.000Z  304.180  304.745  304.120  304.210
2  2020-06-01T14:00:00.000Z  304.800  305.100  303.925  304.270
3  2020-06-01T14:15:00.000Z  304.985  305.085  304.565  304.820
4  2020-06-01T14:30:00.000Z  305.250  305.295  304.900  305.025
```

### Crypto Data

```
>>> c = Crypto.from_env()
>>> c.get_top("btcusd")
[{'ticker': 'btcusd', 'baseCurrency': 'btc', 'quoteCurrency': 'usd', 'topOfBookData': [{'quoteTimestamp': '2022-07-12T00:56:33.039406+00:00', 'lastSaleTimestamp': '2022-07-12T00:54:45.080000+00:00', 'bidSize': 0.135, 'bidPrice': 19802.719, 'askSize': 0.0282, 'askPrice': 19800.3, 'lastSize': 0.00095135, 'lastSizeNotional': 18.8441828759, 'lastPrice': 19807.834, 'bidExchange': 'BITTREX', 'askExchange': 'KRAKEN', 'lastExchange': 'BITTREX'}]}]

>>> df = c.get_prices(ticker="btcusd", start_date="2020-06-01", end_date="2022-06-01", resample_freq="30min")
>>> df.head()
                        date         open  ...  volumeNotional  tradesDone
0  2020-06-01T00:00:00+00:00  9447.655840  ...    1.319688e+07     16512.0
1  2020-06-01T00:30:00+00:00  9486.461436  ...    8.264942e+06     12032.0
2  2020-06-01T01:00:00+00:00  9498.238963  ...    8.489034e+06     12159.0
3  2020-06-01T01:30:00+00:00  9495.926994  ...    1.628270e+07     16646.0
4  2020-06-01T02:00:00+00:00  9551.179766  ...    1.456345e+07     14843.0

[5 rows x 8 columns]
```