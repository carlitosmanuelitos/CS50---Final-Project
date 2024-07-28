import yfinance as yf
from app.models import Stock, StockMetadata
from app import db

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'current_price': info.get('currentPrice'),
            'company_name': info.get('longName'),
            'industry': info.get('industry'),
            'market_cap': info.get('marketCap'),
            'ceo': info.get('ceo'),
            'revenue': info.get('totalRevenue'),
            'debt': info.get('totalDebt'),
            'description': info.get('longBusinessSummary')
        }
    except:
        return None

def update_stock_prices(portfolio):
    for stock in portfolio.stocks:
        data = get_stock_data(stock.ticker)
        if data:
            stock.current_price = data['current_price']
            
            # Update or create StockMetadata
            metadata = StockMetadata.query.get(stock.ticker)
            if not metadata:
                metadata = StockMetadata(ticker=stock.ticker)
            
            metadata.company_name = data['company_name']
            metadata.industry = data['industry']
            metadata.market_cap = data['market_cap']
            metadata.ceo = data['ceo']
            metadata.revenue = data['revenue']
            metadata.debt = data['debt']
            metadata.description = data['description']
            
            db.session.add(metadata)
    
    db.session.commit()