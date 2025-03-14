import yfinance as yf
import pandas as pd
pd.options.display.max_rows = 999
ticker = 'LVMH'
stock = yf.Ticker(ticker)

# print(stock.balance_sheet)
# print(stock.incomestmt)
# print(stock.cashflow)

stock = yf.Ticker(ticker)
info = stock.info

# Fetching financial data
company_name = info.get('longName')
industry = info.get('industry')
market_cap = info.get('marketCap')
currency = info.get('currency')

# Value
current_price = info.get('currentPrice')
per = info.get('trailingPE')

# Return on investment
roe = info.get('returnOnEquity')
roa = info.get('returnOnAssets')

# Earnings
fcf = stock.cash_flow.loc["Free Cash Flow"].iloc[0]
total_revenue = info.get('totalRevenue')
net_income = stock.incomestmt.loc['Net Income'].iloc[0]
gross_margin = info.get('grossMargins')
operating_margin = info.get('operatingMargins')
net_margin = info.get('profitMargins')

# Shareholder
dividend_yield = info.get('dividendYield', 0)

# Balance sheet
total_debt = info.get('totalDebt')
total_equity = total_equity = stock.balance_sheet.loc["Stockholders Equity"].iloc[0]
cash = info.get('totalCash')
total_assets = stock.balance_sheet.loc['Total Assets'].iloc[0]

try:
    current_liabilities = stock.balance_sheet.loc['Current Liabilities'].iloc[0]
except:
    current_liabilities = stock.balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0]

# Per share
shares_outstanding = info.get('sharesOutstanding')
revenue_per_share = info.get('revenuePerShare')
earnings_per_share = info.get('trailingEps')
fcf_per_share = (fcf / shares_outstanding)

# Calculate additional metrics
fcf_yield = (fcf / market_cap)
price_to_fcf = (current_price / (fcf / shares_outstanding))
freecashflow_margin = (fcf / total_revenue)

print("DONE")
