"""
Main routes for the Stock AI Portfolio Tracking app.

This module handles the main functionality of the application, including the home page,
user profile, investment survey, and dashboard. It defines routes for these features
and interacts with the database to store and retrieve user data.

Routes:
    /: Home page
    /profile: User profile page
    /investment-survey: Investment profile survey
    /update-profile: Update user profile
    /dashboard: User dashboard

Functions:
    index: Render the home page
    profile: Render the user profile page
    investment_survey: Handle the investment profile survey
    update_profile: Handle user profile updates
    dashboard: Render the user dashboard
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import User, Portfolio, InvestmentProfile
from app import db
from datetime import datetime
from app.forms.profile_forms import InvestmentSurveyForm, UpdateProfileForm  # Add this import

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/investment-survey', methods=['GET', 'POST'])
@login_required
def investment_survey():
    form = InvestmentSurveyForm(obj=current_user.investment_profile)
    
    if form.validate_on_submit():
        if current_user.investment_profile:
            form.populate_obj(current_user.investment_profile)
            current_user.investment_profile.last_updated = datetime.utcnow()
        else:
            new_profile = InvestmentProfile(user_id=current_user.id)
            form.populate_obj(new_profile)
            db.session.add(new_profile)
        
        db.session.commit()
        flash('Investment profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    return render_template('investment_survey.html', form=form)

@main.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('update_profile.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    # Implement dashboard logic here
    return render_template('dashboard.html')