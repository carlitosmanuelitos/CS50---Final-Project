from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models import Portfolio, Stock
from app.forms.portfolio_forms import AddStockForm
from app.utility.yfinance_utils import update_stock_prices

portfolio = Blueprint('portfolio', __name__)



@portfolio.route('/portfolio', methods=['GET', 'POST'])
@login_required
def view_portfolio():
    # Ensure the user has a portfolio
    if not current_user.portfolio:
        new_portfolio = Portfolio(owner=current_user, name=f"{current_user.username}'s Portfolio")
        db.session.add(new_portfolio)
        db.session.commit()
        flash('A new portfolio has been created for you.', 'info')

    form = AddStockForm()
    if form.validate_on_submit():
        stock = Stock(
            ticker=form.ticker.data.upper(),
            shares=form.shares.data,
            purchase_price=form.purchase_price.data,
            purchase_date=form.purchase_date.data,
            portfolio_id=current_user.portfolio.id
        )
        stock.update_price()  # Fetch current price from yfinance
        db.session.add(stock)
        db.session.commit()
        flash(f'Stock {stock.ticker} added to your portfolio!', 'success')
        return redirect(url_for('portfolio.view_portfolio'))

    user_portfolio = current_user.portfolio
    stocks = user_portfolio.stocks.all()
    if request.method == 'POST' and 'update_prices' in request.form:
        tickers = [stock.ticker for stock in stocks]
        updated_prices = update_stock_prices(tickers)
        for stock in stocks:
            stock.current_price = updated_prices.get(stock.ticker, stock.current_price)
        db.session.commit()
        flash('Stock prices updated!', 'success')

    return render_template('portfolio.html', form=form, stocks=stocks, portfolio=user_portfolio)

@portfolio.route('/portfolio/remove/<int:stock_id>', methods=['POST'])
@login_required
def remove_stock(stock_id):
    stock = Stock.query.get_or_404(stock_id)
    if stock.portfolio.user_id != current_user.id:
        flash('You do not have permission to remove this stock.', 'danger')
        return redirect(url_for('portfolio.view_portfolio'))
    
    db.session.delete(stock)
    db.session.commit()
    flash(f'Stock {stock.ticker} removed from your portfolio.', 'success')
    return redirect(url_for('portfolio.view_portfolio'))

# Add more portfolio-related routes here as needed