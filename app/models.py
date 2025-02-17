from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    portfolios = db.relationship('Portfolio', backref='owner', lazy='dynamic')
    investment_profile = db.relationship('InvestmentProfile', backref='user', uselist=False)
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stocks = db.relationship('Stock', backref='portfolio', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def total_value(self):
        return sum(stock.current_value for stock in self.stocks)

    @property
    def total_gain_loss(self):
        return sum(stock.gain_loss for stock in self.stocks)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    ticker = db.Column(db.String(10), index=True)
    company_name = db.Column(db.String(100))
    shares = db.Column(db.Float)
    purchase_price = db.Column(db.Float)
    current_price = db.Column(db.Float)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def current_value(self):
        return self.shares * self.current_price

    @property
    def gain_loss(self):
        return self.current_value - (self.shares * self.purchase_price)

    @property
    def gain_loss_percentage(self):
        if self.purchase_price > 0:
            return (self.current_price - self.purchase_price) / self.purchase_price * 100
        return 0

class StockMetadata(db.Model):
    ticker = db.Column(db.String(10), primary_key=True)
    company_name = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    market_cap = db.Column(db.Float)
    ceo = db.Column(db.String(100))
    revenue = db.Column(db.Float)
    debt = db.Column(db.Float)
    description = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class InvestmentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    risk_tolerance = db.Column(db.Integer)
    annual_income = db.Column(db.Float)
    monthly_investment = db.Column(db.Float)
    net_worth = db.Column(db.Float)
    preferred_industries = db.Column(db.String(200))
    age = db.Column(db.Integer)
    education_level = db.Column(db.String(50))
    country = db.Column(db.String(2))
    investment_horizon = db.Column(db.String(20))
    investment_experience = db.Column(db.String(3))
    years_investing = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    ticker = db.Column(db.String(10), index=True)
    transaction_type = db.Column(db.String(4))  # 'buy' or 'sell'
    shares = db.Column(db.Float)
    price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def total_value(self):
        return self.shares * self.price