#Data.py
'''
- Download Stock and Option Data or use local data file
- Functions to query/return subset by date / ticker / other criteria
'''
from polygon import RESTClient
import pandas as pd
# import pandas_ta as ta
# from backtesting import Strategy
# from backtesting.lib import crossover
# from backtesting import Backtest
# from ta.momentum import RSIIndicator

client = RESTClient(api_key="SOlnh6Eqtscpw7z1QVTDNKwPUh_n6ZYm")

def get_stock_prices(ticker, client, from_date, to_date):
    # return a pandas dataframe with: date, high, low, open, close, volume
    '''
    polygon.io API: dailyStockData[n] attributes:
    ['close', 'from_dict', 'high', 'low', 'open', 
    'otc', 'timestamp', 'transactions', 
    'volume', 'vwap']
    '''
    dailyStockData = client.list_aggs(ticker=ticker, multiplier=1, timespan='day',
                                  from_=from_date,
                                  to = to_date)
    prices = []
    # put polygon stock data into list of tuples
    for d in dailyStockData:
        prices.append((d.high, d.low, d.open, d.close, d.timestamp, d.volume))
    print(f'Found {len(prices)} records')
    # load the list of tuples into a pandas dataframe
    columns = ['High', 'Low', 'Open', 'Close', 'Timestamp', 'Volume']
    df = pd.DataFrame(prices, columns=columns)
    # convert epoch time to pandas datetime, set as index, drop Timestamp column
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df = df.set_index('Date')
    df= df.drop('Timestamp', axis=1)
    # round volume to integer
    df['Volume'] = pd.to_numeric(df['Volume'], downcast='integer', errors='coerce')
    return df
