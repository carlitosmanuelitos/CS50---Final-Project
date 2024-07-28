"""
Profile and investment survey forms for the Stock AI Portfolio Tracking app.

This module defines the forms used for updating user profiles and completing
the investment survey. It uses Flask-WTF for form handling and validation.

Classes:
    InvestmentSurveyForm: Form for the investment profile survey
    UpdateProfileForm: Form for updating user profile information
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Length

class InvestmentSurveyForm(FlaskForm):
    risk_tolerance = SelectField('Risk Tolerance', choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')], validators=[DataRequired()])
    annual_income = FloatField('Annual Income', validators=[DataRequired(), NumberRange(min=0)])
    monthly_investment = FloatField('Monthly Investment', validators=[DataRequired(), NumberRange(min=0)])
    net_worth = FloatField('Net Worth', validators=[DataRequired(), NumberRange(min=0)])
    preferred_industries = StringField('Preferred Industries', validators=[Length(max=200)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=120)])
    education_level = SelectField('Education Level', choices=[('high_school', 'High School'), ('bachelor', 'Bachelor'), ('master', 'Master'), ('phd', 'PhD')], validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired(), Length(max=2)])
    investment_horizon = SelectField('Investment Horizon', choices=[('short', 'Short-term'), ('medium', 'Medium-term'), ('long', 'Long-term')], validators=[DataRequired()])
    investment_experience = SelectField('Investment Experience', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], validators=[DataRequired()])
    years_investing = IntegerField('Years Investing', validators=[NumberRange(min=0)])
    submit = SubmitField('Update Investment Profile')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Update Profile')