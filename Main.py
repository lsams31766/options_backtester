#Main.py
from Data import client, get_stock_prices
'''
- Retrieve Stock and Option data using Data.py module
- Runtart a back test, given parmeters including strategy
- Retrieve the trade data
- Retrieve the results of the back test
- Represent Data via Table
- Represent data via Chart
'''

ticker = 'AAPL'
df = get_stock_prices(ticker,client,'2024-01-01','2024-12-31')
print(df.head())
