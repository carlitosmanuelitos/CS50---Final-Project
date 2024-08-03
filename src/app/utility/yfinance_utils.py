import yfinance as yf
from datetime import datetime

def get_stock_data(ticker):
    """
    Fetch stock data from yfinance API.
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

def update_stock_prices(tickers):
    """
    Update current prices for a list of stock tickers.
    """
    updated_data = {}
    for ticker in tickers:
        data = get_stock_data(ticker)
        updated_data[ticker] = data['current_price']
    return updated_data

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
    
    
