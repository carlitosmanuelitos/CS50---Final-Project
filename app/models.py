from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    portfolios = db.relationship('Portfolio', backref='owner', lazy='dynamic')
    investment_profile = db.relationship('InvestmentProfile', backref='user', uselist=False)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stocks = db.relationship('Stock', backref='portfolio', lazy='dynamic')

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), index=True)
    shares = db.Column(db.Float)
    purchase_price = db.Column(db.Float)
    purchase_date = db.Column(db.DateTime)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))

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
    last_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())