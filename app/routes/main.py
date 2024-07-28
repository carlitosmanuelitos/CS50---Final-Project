from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import User, Portfolio, InvestmentProfile
from app import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if not current_user.investment_profile:
        return redirect(url_for('main.investment_survey'))
    return render_template('dashboard.html')


@main.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')

@main.route('/ai-recommendations')
@login_required
def ai_recommendations():
    return render_template('ai_recommendations.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/investment-survey', methods=['GET', 'POST'])
@login_required
def investment_survey():
    existing_profile = current_user.investment_profile

    if request.method == 'POST':
        if existing_profile:
            # Update existing profile
            existing_profile.risk_tolerance = request.form.get('risk_tolerance')
            existing_profile.annual_income = float(request.form.get('annual_income'))
            existing_profile.monthly_investment = float(request.form.get('monthly_investment'))
            existing_profile.net_worth = float(request.form.get('net_worth'))
            existing_profile.preferred_industries = ','.join(request.form.getlist('preferred_industries'))
            existing_profile.age = int(request.form.get('age'))
            existing_profile.education_level = request.form.get('education_level')
            existing_profile.country = request.form.get('country')
            existing_profile.investment_horizon = request.form.get('investment_horizon')
            existing_profile.investment_experience = request.form.get('investment_experience')
            existing_profile.years_investing = int(request.form.get('years_investing') or 0)
            existing_profile.last_updated = datetime.utcnow()
        else:
            # Create new profile
            new_profile = InvestmentProfile(
                user_id=current_user.id,
                risk_tolerance=request.form.get('risk_tolerance'),
                annual_income=float(request.form.get('annual_income')),
                monthly_investment=float(request.form.get('monthly_investment')),
                net_worth=float(request.form.get('net_worth')),
                preferred_industries=','.join(request.form.getlist('preferred_industries')),
                age=int(request.form.get('age')),
                education_level=request.form.get('education_level'),
                country=request.form.get('country'),
                investment_horizon=request.form.get('investment_horizon'),
                investment_experience=request.form.get('investment_experience'),
                years_investing=int(request.form.get('years_investing') or 0)
            )
            db.session.add(new_profile)

        db.session.commit()
        flash('Investment profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    return render_template('investment_survey.html', profile=existing_profile)

@main.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('update_profile.html', user=current_user)