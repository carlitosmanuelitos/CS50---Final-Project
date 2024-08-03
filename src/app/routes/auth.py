"""
Authentication routes for the Stock AI Portfolio Tracking app.

This module handles user registration, login, and logout functionality. It defines
routes for user authentication and uses Flask-Login for managing user sessions.

Routes:
    /register: Handle user registration
    /login: Handle user login
    /logout: Handle user logout

Functions:
    register: Handle user registration process
    login: Handle user login process
    logout: Handle user logout process
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, Portfolio
from .. import db
from ..forms.auth_forms import RegisterForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data, username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.flush()  # This assigns an ID to the user
        new_portfolio = Portfolio(owner=new_user, name=f"{new_user.username}'s Portfolio")
        db.session.add(new_portfolio)
        db.session.commit()
        return render_template('login.html', form=LoginForm(), show_notification=True, notification_message='Registration successful. Please log in.')
    
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not user.has_completed_survey:
                return redirect(url_for('main.investment_survey'))
            return redirect(next_page or url_for('main.dashboard'))
        flash('Invalid email or password. Please try again.', 'error')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.index'))