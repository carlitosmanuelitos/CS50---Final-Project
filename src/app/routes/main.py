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
from ..models import User, Portfolio, InvestmentProfile
from .. import db
from datetime import datetime
from ..forms.profile_forms import InvestmentSurveyForm, UpdateProfileForm

# ... rest of the file remains the same

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():

    return render_template('dashboard.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm(obj=current_user)
    investment_profile = InvestmentProfile.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('profile.html', form=form, user=current_user, investment_profile=investment_profile)


@main.route('/investment-survey', methods=['GET', 'POST'])
@login_required
def investment_survey():
    profile = InvestmentProfile.query.filter_by(user_id=current_user.id).first()
    form = InvestmentSurveyForm(obj=profile) if profile else InvestmentSurveyForm()
    
    if form.validate_on_submit():
        if not profile:
            profile = InvestmentProfile(user_id=current_user.id)
        
        try:
            form.populate_obj(profile)
            
            # Handle multi-select fields
            profile.preferred_industries = ','.join(form.preferred_industries.data)
            profile.secondary_investment_goals = ','.join(form.secondary_investment_goals.data)
            
            # Handle boolean fields
            profile.sustainable_investing = form.sustainable_investing.data == 'yes'
            profile.has_existing_portfolio = form.has_existing_portfolio.data == 'yes'
            
            db.session.add(profile)
            current_user.has_completed_survey = True
            db.session.commit()
            flash('Your investment profile has been updated successfully.', 'success')
            return redirect(url_for('main.profile'))
        except Exception as e:
            db.session.rollback()
            print(f"Error saving profile: {str(e)}")
            flash('An error occurred while saving your profile. Please try again.', 'error')
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'error')
    
    return render_template('investment_survey.html', form=form)