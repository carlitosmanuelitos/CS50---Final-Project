"""
Database models for the Stock AI Portfolio Tracking app.

This module defines the database schema using SQLAlchemy ORM. It includes models for
users, portfolios, stocks, stock metadata, investment profiles, and transactions.
"""

from src.app import db
from werkzeug.security import generate_password_hash, check_password_hash
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
    has_completed_survey = db.Column(db.Boolean, default=False)


    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class InvestmentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    
    # Personal Information
    age = db.Column(db.Integer)
    country = db.Column(db.String(2))
    education_level = db.Column(db.String(20))
    
    # Financial Information
    annual_income = db.Column(db.Float)
    monthly_investment = db.Column(db.Float)
    net_worth = db.Column(db.Float)
    
    # Investment Preferences
    risk_tolerance = db.Column(db.Integer)
    investment_horizon = db.Column(db.String(20))
    preferred_industries = db.Column(db.String(200))  # Store as comma-separated values
    investment_experience = db.Column(db.Integer)
    years_investing = db.Column(db.Integer)
    
    # Investment Goals
    primary_investment_goal = db.Column(db.String(50))
    secondary_investment_goals = db.Column(db.String(200))  # Store as comma-separated values
    sustainable_investing = db.Column(db.Boolean)
    
    # Portfolio Review
    has_existing_portfolio = db.Column(db.Boolean)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<InvestmentProfile {self.user_id}>'

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