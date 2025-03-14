import yfinance as yf
import dotenv
import os
import psycopg2
from psycopg2 import sql
from tqdm import tqdm

dotenv.load_dotenv()

def get_financial_data(ticker):

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

    sql_query = f"""
    INSERT INTO financial_data (
        ticker, company_name, industry, market_cap, currency, current_price, per, roe, roa, fcf, total_revenue, net_income, 
        gross_margin, operating_margin, net_margin, dividend_yield, total_debt, total_equity, cash, total_assets, 
        current_liabilities, shares_outstanding, revenue_per_share, earnings_per_share, fcf_per_share, fcf_yield, 
        price_to_fcf, freecashflow_margin
    ) VALUES (
        '{ticker}', '{company_name}', '{industry}', {market_cap}, '{currency}', {current_price}, {per}, {roe}, {roa}, {fcf}, 
        {total_revenue}, {net_income}, {gross_margin}, {operating_margin}, {net_margin}, {dividend_yield}, {total_debt}, 
        {total_equity}, {cash}, {total_assets}, {current_liabilities}, {shares_outstanding}, {revenue_per_share}, 
        {earnings_per_share}, {fcf_per_share}, {fcf_yield}, {price_to_fcf}, {freecashflow_margin}
    )
    """
    return sql_query

def insert_into_financial_data_table(sql_query):
    try:
        # Connect to your postgres DB
        connection = psycopg2.connect(
            dbname=os.getenv("PGDATABASE"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            host=os.getenv("PGHOST"),
            port="5432",
            sslmode="require"
        )

        cursor = connection.cursor()
        
        # Execute the SQL query
        cursor.execute(sql_query)
        
        # Commit the transaction
        connection.commit()
        
        # print("Data inserted successfully")
        
    except Exception as error:
        print(f"Error: {error}")
        
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_tickers():
    try:
        # Connect to your postgres DB
        connection = psycopg2.connect(
            dbname=os.getenv("PGDATABASE"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            host=os.getenv("PGHOST"),
            port="5432",
            sslmode="require"
        )

        cursor = connection.cursor()
        
        # Execute the SQL query
        cursor.execute("SELECT ticker FROM assets WHERE category = 'Stock'")
        
        # Fetch the data
        tickers = cursor.fetchall()
        
        # Extract tickers from the fetched data
        tickers = [ticker[0] for ticker in tickers]
        
        return tickers
    
    except Exception as error:
        print(f"Error: {error}")
        
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

tickers_list = get_tickers()
# tickers_list = ['BRK.B']
for ticker in tqdm(tickers_list):

    try:
        sql_query = get_financial_data(ticker)
        insert_into_financial_data_table(sql_query)
    except Exception as e:
        print(ticker)
        print(sql_query)