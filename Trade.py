#Trad.py
# Try some sample trades
from Data import *

# helper functions
def get_stock_open_close_prices(ticker, date, next_date):
    # get 2 stock prices, the opening on dates inidicated
    df = get_stock_prices(ticker,client,date,next_date)
    day_1_row = df.index[0]
    day_2_row = df.index[1]
    if ticker == 'SPY':
        open_price = df.loc[day_1_row, 'Open'] * 10
        close_price = df.loc[day_2_row, 'Open'] * 10
    else:
        open_price = df.loc[day_1_row, 'Open']
        close_price = df.loc[day_2_row, 'Open']
    return open_price, close_price

# Stregies

def ZeroDTE_Credit_Spread(ticker, date, next_date):
    # Credit Spread is: SELL PUT 6 SP's above underlying
    # BUY PUT 3 SP's below that
    #### Get stock prices ####
    open_price, close_price = get_stock_open_close_prices(ticker, date, next_date)
    print(f'Ticker: {ticker}, Open: {open_price}, Close: {close_price}')

    #### Get Strike prices ####
    # need options prices 3 and 6 strikes avove middle price
    SP_above, SP_below = get_strike_prices_for_ticker(open_price,ticker,10,split_results=True)
    print(f'SPs are: {SP_above} and {SP_below}')
    #exit(0)

    #### Get options prices ####
    SP_1 = SP_above[6] # 6 Strike Prices above middle
    SP_2 = SP_above[3] # 3 Strike Prices above middle
    options_ticker1 =  create_options_ticker(ticker, date, 'put', SP_1)
    options_ticker2 = create_options_ticker(ticker, date, 'put', SP_2)
    print(f'Options tickers are: {options_ticker1} and {options_ticker2}')
    options_price1 = get_options_chain_data(options_ticker1, date, next_date)
    options_price2 = get_options_chain_data(options_ticker2, date, next_date)
    print(f'SELL PUT SP={SP_1} on {date}, Open price: {options_price1}')
    print(f'BUY PUT SP={SP_2} on {date}, Open price: {options_price2}')

    #### Calculate max profit, max loss ####
    # Note sell we get premium, buy we pay premimum
    net_premium = options_price1 - options_price2
    print(f'MAX profit is {net_premium}')
    # Max loss is SP1-SP2-Premium
    max_loss = SP_1-SP_2-net_premium
    print(f'MAX loss is {max_loss}')


    #### get Trade results based on stock prices ####
    #short_pnl = Premuium1-MAX(0,strikePrice1-Final_price)
    short_pnl = options_price1 - max(0, SP_1-close_price)
    #long_pnl = MAX(StrikePrice2-Final_price,0)-Premium2
    long_pnl = max(0,SP_2-close_price) - options_price2
    final_pnl = short_pnl + long_pnl
    print(f'Trade results: Short: {short_pnl}, Long: {long_pnl}, Total: {final_pnl}')
    # TODO save trade to trades table 
    # TODO save PNL to running PNL, for now return PNL for back testing
    return final_pnl
 
