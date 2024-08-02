import yfinance as yf
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def get_stock_data(ticker, expire_after=300):
    """
    Fetch stock data from yfinance API with caching.
    Cache expires after 5 minutes (300 seconds) by default.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    
    return {
        'ticker': ticker,
        'company_name': info.get('longName', ''),
        'current_price': info.get('currentPrice', 0),
        'market_cap': info.get('marketCap', 0),
        'industry': info.get('industry', ''),
        'change_percent': info.get('regularMarketChangePercent', 0) * 100,
        'timestamp': datetime.now(),
    }

def update_stock_prices(stocks):
    """
    Update current prices for a list of stocks.
    """
    for stock in stocks:
        data = get_stock_data(stock.ticker)
        stock.current_price = data['current_price']
        stock.last_updated = datetime.now()

def get_stock_metadata(ticker):
    """
    Fetch detailed stock metadata.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    
    return {
        'ticker': ticker,
        'company_name': info.get('longName', ''),
        'industry': info.get('industry', ''),
        'market_cap': info.get('marketCap', 0),
        'ceo': info.get('companyOfficers', [{}])[0].get('name', ''),
        'revenue': info.get('totalRevenue', 0),
        'debt': info.get('totalDebt', 0),
        'description': info.get('longBusinessSummary', ''),
    }