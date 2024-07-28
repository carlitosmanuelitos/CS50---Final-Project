from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Portfolio, Stock, Transaction, StockMetadata
from app import db
from app.services.stock_service import get_stock_data, update_stock_prices
from app.services.portfolio_service import calculate_portfolio_stats

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@portfolio_bp.route('/')
@login_required
def portfolio():
    user_portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
    return render_template('portfolio.html', portfolios=user_portfolios)

@portfolio_bp.route('/<int:portfolio_id>')
@login_required
def portfolio_detail(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.user_id != current_user.id:
        flash('You do not have access to this portfolio.', 'error')
        return redirect(url_for('portfolio.portfolio'))
    
    update_stock_prices(portfolio)
    stats = calculate_portfolio_stats(portfolio)
    
    return render_template('portfolio_detail.html', portfolio=portfolio, stats=stats)

@portfolio_bp.route('/create', methods=['POST'])
@login_required
def create_portfolio():
    name = request.form.get('name')
    if not name:
        flash('Portfolio name is required.', 'error')
        return redirect(url_for('portfolio.portfolio'))
    
    new_portfolio = Portfolio(name=name, user_id=current_user.id)
    db.session.add(new_portfolio)
    db.session.commit()
    flash(f'Portfolio "{name}" created successfully.', 'success')
    return redirect(url_for('portfolio.portfolio'))

@portfolio_bp.route('/<int:portfolio_id>/add_stock', methods=['POST'])
@login_required
def add_stock(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.user_id != current_user.id:
        flash('You do not have access to this portfolio.', 'error')
        return redirect(url_for('portfolio.portfolio'))
    
    ticker = request.form.get('ticker')
    shares = float(request.form.get('shares'))
    
    stock_data = get_stock_data(ticker)
    if not stock_data:
        flash(f'Could not fetch data for stock {ticker}.', 'error')
        return redirect(url_for('portfolio.portfolio_detail', portfolio_id=portfolio_id))
    
    new_stock = Stock(
        portfolio_id=portfolio_id,
        ticker=ticker,
        company_name=stock_data['company_name'],
        shares=shares,
        purchase_price=stock_data['current_price'],
        current_price=stock_data['current_price']
    )
    db.session.add(new_stock)
    
    transaction = Transaction(
        user_id=current_user.id,
        portfolio_id=portfolio_id,
        ticker=ticker,
        transaction_type='buy',
        shares=shares,
        price=stock_data['current_price']
    )
    db.session.add(transaction)
    
    db.session.commit()
    flash(f'Successfully added {shares} shares of {ticker} to your portfolio.', 'success')
    return redirect(url_for('portfolio.portfolio_detail', portfolio_id=portfolio_id))

@portfolio_bp.route('/<int:portfolio_id>/sell_stock', methods=['POST'])
@login_required
def sell_stock(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.user_id != current_user.id:
        flash('You do not have access to this portfolio.', 'error')
        return redirect(url_for('portfolio.portfolio'))
    
    stock_id = request.form.get('stock_id')
    shares_to_sell = float(request.form.get('shares'))
    
    stock = Stock.query.get_or_404(stock_id)
    if stock.portfolio_id != portfolio_id:
        flash('This stock does not belong to the selected portfolio.', 'error')
        return redirect(url_for('portfolio.portfolio_detail', portfolio_id=portfolio_id))
    
    if shares_to_sell > stock.shares:
        flash('You cannot sell more shares than you own.', 'error')
        return redirect(url_for('portfolio.portfolio_detail', portfolio_id=portfolio_id))
    
    stock_data = get_stock_data(stock.ticker)
    if not stock_data:
        flash(f'Could not fetch current price for stock {stock.ticker}.', 'error')
        return redirect(url_for('portfolio.portfolio_detail', portfolio_id=portfolio_id))
    
    stock.shares -= shares_to_sell
    if stock.shares == 0:
        db.session.delete(stock)
    
    transaction = Transaction(
        user_id=current_user.id,
        portfolio_id=portfolio_id,
        ticker=stock.ticker,
        transaction_type='sell',
        shares=shares_to_sell,
        price=stock_data['current_price']
    )
    db.session.add(transaction)
    
    db.session.commit()
    flash(f'Successfully sold {shares_to_sell} shares of {stock.ticker}.', 'success')
    return redirect(url_for('portfolio.portfolio_detail', portfolio_id=portfolio_id))

@portfolio_bp.route('/stock_search')
@login_required
def stock_search():
    query = request.args.get('query', '')
    stocks = StockMetadata.query.filter(
        (StockMetadata.ticker.ilike(f'%{query}%')) |
        (StockMetadata.company_name.ilike(f'%{query}%'))
    ).limit(10).all()
    
    results = [{'ticker': stock.ticker, 'company_name': stock.company_name} for stock in stocks]
    return jsonify(results)


from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Portfolio, Stock, Transaction, StockMetadata
from app import db
from app.services.stock_service import get_stock_data, update_stock_prices
from app.services.portfolio_service import calculate_portfolio_stats

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/portfolio')

@portfolio_bp.route('/')
@login_required
def portfolio():
    user_portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
    return render_template('portfolio.html', portfolios=user_portfolios)

@portfolio_bp.route('/create', methods=['POST'])
@login_required
def create_portfolio():
    name = request.form.get('name')
    if not name:
        flash('Portfolio name is required.', 'error')
        return redirect(url_for('portfolio.portfolio'))
    
    new_portfolio = Portfolio(name=name, user_id=current_user.id)
    db.session.add(new_portfolio)
    db.session.commit()
    flash(f'Portfolio "{name}" created successfully.', 'success')
    return redirect(url_for('portfolio.portfolio'))