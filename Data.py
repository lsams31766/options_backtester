#Data.py
'''
- Download Stock and Option Data or use local data file
- Functions to query/return subset by date / ticker / other criteria
'''
from polygon import RESTClient
import pandas as pd
client = RESTClient(api_key="SOlnh6Eqtscpw7z1QVTDNKwPUh_n6ZYm")

def create_options_ticker(stock_ticker, expiration_date, option_type, strike_price):
    """
    Create an options ticker symbol based on the given parameters.
    
    Args:
        stock_ticker (str): The symbol of the underlying stock (e.g., 'AAPL', 'SPY').
        expiration_date (str): The expiration date in 'YYYY-MM-DD' format (e.g., '2024-01-02').
        option_type (str): The option type ('call' or 'put').
        strike_price (float): The strike price of. the option (e.g., 150.50).
    
    Returns:
        str: The formatted options ticker symbol.
    """
    
    # Convert expiration date to YYMMDD format
    expiration_date_obj = str(expiration_date).split('-')
    exp_date3 = expiration_date_obj[2].split(' ')[0]
    # third piece has time, remove it
    expiration_yy_mm_dd = expiration_date_obj[0][2:] + expiration_date_obj[1] + exp_date3    
    # Option type (Call = 'C', Put = 'P')
    if option_type.lower() == 'call':
        option_type = 'C'
    elif option_type.lower() == 'put':
        option_type = 'P'
    else:
        raise ValueError("Option type must be either 'call' or 'put'.")
    
    # Format strike price: Remove the decimal point and ensure it's an integer string
    strike_price_str = str(int(str(strike_price).replace('.', '')))
    # add the zeros we need
    # many need logic based on size of sp
    if strike_price < 1000:
        strike_price_str = f'00{strike_price_str}000'
    else:
        strike_price_str = f'00{strike_price_str}00'
    
    # Construct the options ticker
    options_ticker = f"{stock_ticker}{expiration_yy_mm_dd}{option_type}{strike_price_str}"
    
    return 'O:' + options_ticker # O: needed for polygon.io

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

# IT seems we cannot get the strike prices for a expired options contract
# so we need to estimate and check if we get data

def get_strike_prices_for_ticker(stock_price, ticker, nbr_strikes, split_results=False):
    # if stock_price > 5000, assume SP's every 5 for SPX
    # try to get 10 above and 10 below
    if stock_price > 99  and ticker == 'SPY':
        # 5868  round to nearest 5
        middle = int(stock_price - (stock_price % 5))
        print('middle is',middle)
        # make list 10 up by 5
        L = list(range(middle,middle+55,nbr_strikes/2))
        # make list 10 down by 5
        M = list(range(middle-5,middle-55,nbr_strikes/2))
    if stock_price > 99  and ticker == 'QQQ':
        # 5868  round to nearest 5
        middle = int(stock_price - (stock_price % 1))
        print('middle is',middle)
        L = list(range(middle,middle+12,1))
        M = list(range(middle-1,middle-12,-1))
    if split_results == False:
        return sorted(L + M)
    else:
        return L,M


def get_options_prices(data):
    # return polygon client data to get date, high, low, open, close, volume
    '''
    polygon.io API: Agg data:
      [Agg(open=2.08, high=2.7, low=1.97, close=2.29, volume=1614, 
        timestamp=1731420000000), 
        Agg(open=2.25, high=2.57, low=1.8, close=2.02, volume=2168,
        timestamp=173142360000), ...
    '''
    # put polygon stock data into list of tuples
    prices = []
    for d in data:
        prices.append((d.high, d.low, d.open, d.close, d.timestamp, d.volume))
    # print(f'Found {len(prices)} records')
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

def get_options_chain_data(ticker, from_ = '2024-01-01', to = '2024-01-03', hour_index=0):
    # hour index is the hour offset from first one
    dailyOptionsData = client.get_aggs(ticker = ticker, 
                    multiplier=1,
                    timespan= 'hour',
                    from_ = from_,
                    to = to)
    # save the data as pandas dataframe
    print("OPTIONS for ticker: ", ticker)
    df = get_options_prices(dailyOptionsData)
    # just the hour offset row, the open value for now
    the_time = df.index[hour_index]
    open_price = df.loc[the_time, 'Open']
    return open_price
