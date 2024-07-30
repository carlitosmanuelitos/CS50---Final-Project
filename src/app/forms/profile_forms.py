"""
Profile and investment survey forms for the Stock AI Portfolio Tracking app.

This module defines the forms used for updating user profiles and completing
the investment survey. It uses Flask-WTF for form handling and validation.

Classes:
    InvestmentSurveyForm: Form for the investment profile survey
    UpdateProfileForm: Form for updating user profile information
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SelectMultipleField, SubmitField, HiddenField, RadioField
from wtforms.validators import DataRequired, Email, NumberRange, Length
from wtforms.validators import DataRequired, Optional



from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SelectMultipleField, SubmitField, HiddenField, RadioField
from wtforms.validators import DataRequired, Email, NumberRange, Length, Optional, ValidationError

class InvestmentSurveyForm(FlaskForm):
    # Personal Information
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=120)])
    country = SelectField('Country', 
                          choices = [
        ('US', 'United States'),
        ('UK', 'United Kingdom'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('AL', 'Albania'),
        ('AD', 'Andorra'),
        ('AM', 'Armenia'),
        ('AT', 'Austria'),
        ('AZ', 'Azerbaijan'),
        ('BY', 'Belarus'),
        ('BE', 'Belgium'),
        ('BA', 'Bosnia and Herzegovina'),
        ('BG', 'Bulgaria'),
        ('HR', 'Croatia'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czech Republic'),
        ('DK', 'Denmark'),
        ('EE', 'Estonia'),
        ('FI', 'Finland'),
        ('GE', 'Georgia'),
        ('GR', 'Greece'),
        ('HU', 'Hungary'),
        ('IS', 'Iceland'),
        ('IE', 'Ireland'),
        ('IT', 'Italy'),
        ('KZ', 'Kazakhstan'),
        ('XK', 'Kosovo'),
        ('LV', 'Latvia'),
        ('LI', 'Liechtenstein'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('MT', 'Malta'),
        ('MD', 'Moldova'),
        ('MC', 'Monaco'),
        ('ME', 'Montenegro'),
        ('NL', 'Netherlands'),
        ('MK', 'North Macedonia'),
        ('NO', 'Norway'),
        ('PL', 'Poland'),
        ('PT', 'Portugal'),
        ('RO', 'Romania'),
        ('RU', 'Russia'),
        ('SM', 'San Marino'),
        ('RS', 'Serbia'),
        ('SK', 'Slovakia'),
        ('SI', 'Slovenia'),
        ('ES', 'Spain'),
        ('SE', 'Sweden'),
        ('CH', 'Switzerland'),
        ('TR', 'Turkey'),
        ('UA', 'Ukraine'),
        ('VA', 'Vatican City')
    ])
    education_level = SelectField('Education Level', choices=[
        ('high_school', 'High School'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD')
    ])

    # Financial Information
    annual_income = FloatField('Annual Income (€)', validators=[DataRequired(), NumberRange(min=0)])
    monthly_investment = FloatField('Monthly Investment (€)', validators=[DataRequired(), NumberRange(min=0)])
    net_worth = FloatField('Net Worth (€)', validators=[DataRequired(), NumberRange(min=0)])

    # Investment Preferences
    investment_horizon = RadioField('Investment Horizon', choices=[
        ('short', 'Short-term (0-2 years)'),
        ('medium', 'Medium-term (2-5 years)'),
        ('medium-long', 'Medium-Long term (5-10 years)'),
        ('long', 'Long-term (15 or more years)')
    ])
    preferred_industries = SelectMultipleField('Preferred Industries', choices=[
        ('commodities', 'Commodities'),
        ('health', 'Health Care'),
        ('information_technology', 'Information Technology'),
        ('energy', 'Energy'),
        ('services', 'Services'),
        ('consumer_goods', 'Consumer Goods'),
        ('financials', 'Financials'),
        ('industrials', 'Industrials'),
        ('real_estate', 'Real Estate')
    ])
    
    risk_tolerance = IntegerField('Risk Tolerance', validators=[DataRequired(), NumberRange(min=1, max=5)])
    investment_experience = IntegerField('Investment Experience', validators=[DataRequired(), NumberRange(min=1, max=5)])
    years_investing = IntegerField('Years Investing', validators=[DataRequired(), NumberRange(min=1, max=4)])

    # Investment Goals
    primary_investment_goal = RadioField('Primary Investment Goal', choices=[
        ('capital_appreciation', 'Capital Appreciation'),
        ('income_generation', 'Income Generation'),
        ('capital_preservation', 'Capital Preservation'),
        ('diversification', 'Diversification')
    ])
    secondary_investment_goals = SelectMultipleField('Secondary Investment Goals', choices=[
        ('retirement', 'Retirement Planning'),
        ('education', 'Education Funding'),
        ('home', 'Buying a Home'),
        ('major_purchase', 'Major Purchases'),
        ('travel', 'Travel and Leisure'),
        ('saving', 'Overall Savings')
    ])
    sustainable_investing = RadioField('Are you interested in sustainable or socially responsible investments?', choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ])

    # Portfolio Review
    has_existing_portfolio = RadioField('Do you currently have an investment portfolio?', choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ])

    open_to_higher_risk = RadioField('Are you open to considering slightly higher risk options for potentially better returns?', 
                                     choices=[('yes', 'Yes'), ('no', 'No')],
                                     validators=[Optional()])
    interested_in_growth_stocks = RadioField('Are you interested in growth stocks or other high-risk, high-reward investments?', 
                                             choices=[('yes', 'Yes'), ('no', 'No')],
                                             validators=[Optional()])

    submit = SubmitField('Submit')

    def validate_open_to_higher_risk(self, field):
        if int(self.risk_tolerance.data) <= 2 or self.investment_horizon.data == 'long':
            if not field.data:
                raise ValidationError('This field is required for low risk tolerance or long-term investment horizon.')

    def validate_interested_in_growth_stocks(self, field):
        if int(self.risk_tolerance.data) <= 2 or self.investment_horizon.data == 'long':
            if not field.data:
                raise ValidationError('This field is required for low risk tolerance or long-term investment horizon.')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Update Profile')
    