#Main.py
from Data import *
from Trade import ZeroDTE_Credit_Spread

'''
- Retrieve Stock and Option data using Data.py module
- Runtart a back test, given parmeters including strategy
- Retrieve the trade data
- Retrieve the results of the back test
- Represent Data via Table
- Represent data via Chart
'''

pnl = ZeroDTE_Credit_Spread('QQQ','2024-05-14','2024-05-15')
print('Current PnL', pnl)

# do another trade, calculate running pnl
pnl2 = ZeroDTE_Credit_Spread('QQQ','2024-05-15','2024-05-16')
print('Current PnL', pnl + pnl2)


