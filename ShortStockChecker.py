# Import necessary libraries
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

# Define function to identify stocks to short
def identify_shorts():
    # Define variables
    start_date = datetime.today() - timedelta(days=10)
    end_date = datetime.today() - timedelta(days=1)

    # Get list of S&P 500 stocks
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]

    # Use list comprehension to download stock data for last 10 days
    stocks_data = [yf.download(ticker, start=start_date, end=end_date, interval='1d') for ticker in sp500['Symbol'].tolist()]

    # Combine stock data into a single dataframe
    sp500_data = pd.concat(stocks_data, keys=sp500['Symbol'].tolist(), names=['Symbol', 'Date'])
    sp500_data.reset_index(inplace=True)

    # Calculate daily return
    sp500_data['Return'] = (sp500_data['Close'] - sp500_data['Open']) / sp500_data['Open']

    # Group stock data by symbol and calculate average return and standard deviation
    symbol_data = sp500_data.groupby('Symbol')['Return'].agg(['mean', 'std'])

    # Filter symbol data to only include stocks with consistently negative returns
    shorts = symbol_data[(symbol_data['mean'] < 0) & (symbol_data['mean'] < -2 * symbol_data['std'])]

    # Check for significant negative return using t-test
    shorts = shorts[stats.ttest_1samp(shorts['Return'], 0)[1] < 0.05]

    # Return list of shorts
    return shorts.index.tolist()

# Call function to identify shorts
shorts = identify_shorts()

# Generate alert if shorts are identified
if shorts:
    print("The following stocks are good candidates for shorting: ", shorts)
else:
    print("No stocks were identified as good candidates for shorting.")
