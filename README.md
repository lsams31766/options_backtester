# options_backtester

Requirements:
- Download stock and options data from a source (like polygon.io)
- Create a trade strategy based on time / inidicators / options strategies
- Back Test over a period of time to see if a good PnL vs Hold and Buy is achieved
- Save Trades for later display
- Sage metrics of the Bake Test for later display

Orgainization:

Data Module
- Download Stock and Option Data or use local data file
- Functions to query/return subset by date / ticker / other criteria
  
Processing Module 
- Store multiple strategies on how to trade the equity
- Automate over time period the trades, saving trade data and results

Presentation Module
- Function to start a back test, given parmeters
- Function to retrieve the trade data
- Function to retrieve the results of the back test
- Represent Data via Table
- Represent data via Chart
  
