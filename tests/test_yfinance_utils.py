import pytest
from app.utility.yfinance_utils import get_stock_data, update_stock_prices, get_stock_metadata

def test_get_stock_data():
    data = get_stock_data('AAPL')
    assert data['ticker'] == 'AAPL'
    assert 'company_name' in data
    assert 'current_price' in data
    assert 'market_cap' in data
    assert 'industry' in data
    assert 'change_percent' in data
    assert 'timestamp' in data

def test_update_stock_prices():
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    updated_prices = update_stock_prices(tickers)
    assert len(updated_prices) == 3
    assert all(ticker in updated_prices for ticker in tickers)
    assert all(isinstance(price, (int, float)) for price in updated_prices.values())

def test_get_stock_metadata():
    metadata = get_stock_metadata('AAPL')
    assert metadata['ticker'] == 'AAPL'
    assert 'company_name' in metadata
    assert 'industry' in metadata
    assert 'market_cap' in metadata
    assert 'ceo' in metadata
    assert 'revenue' in metadata
    assert 'debt' in metadata
    assert 'description' in metadata

if __name__ == '__main__':
    pytest.main()