base.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Stock Portfolio Analyzer{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    {% block additional_css %}{% endblock %}
</head>
<body>
    <nav>
        <div class="container">
            <ul>
                <li><a href="{{ url_for('main.dashboard') }}">Dashboard</a></li>
                {% if current_user.is_authenticated %}
                    <li><a href="{{ url_for('portfolio.portfolio') }}">Portfolio</a></li>
                    <li><a href="{{ url_for('main.analytics') }}">Analytics</a></li>
                    <li><a href="{{ url_for('main.ai_recommendations') }}">AI Recommendations</a></li>
                    <li><a href="{{ url_for('main.profile') }}">Profile</a></li>
                    <li><a href="{{ url_for('auth.logout') }}">Logout</a></li>
                {% else %}
                    <li><a href="{{ url_for('auth.login') }}">Login</a></li>
                    <li><a href="{{ url_for('auth.register') }}">Register</a></li>
                {% endif %}
            </ul>
        </div>
    </nav>

    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <ul class="flash-messages">
            {% for category, message in messages %}
                <li class="flash-message {{ category }}">{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    {% block additional_scripts %}{% endblock %}
</body>
</html>


dashboard.html
{% extends "base.html" %}

{% block content %}
<div class="dashboard-container">
    <header class="dashboard-header">
        <h1>Welcome, {{ current_user.username }}!</h1>
        <p>Your Stock Portfolio Dashboard</p>
    </header>

    <div class="dashboard-grid">
        <section class="portfolio-summary">
            <h2>Portfolio Summary</h2>
            {% if current_user.portfolios.all() %}
                <ul>
                {% for portfolio in current_user.portfolios %}
                    <li>
                        <h3>{{ portfolio.name }}</h3>
                        <p>Total Value: $XX,XXX.XX</p>
                        <a href="#" class="button">View Details</a>
                    </li>
                {% endfor %}
                </ul>
            {% else %}
                <p>You don't have any portfolios yet.</p>
            {% endif %}
            <a href="#" class="button">Create New Portfolio</a>
        </section>

        <section class="market-overview">
            <h2>Market Overview</h2>
            <p>Market data will be displayed here.</p>
            <!-- You can add real-time market data here -->
        </section>

        <section class="recent-activity">
            <h2>Recent Activity</h2>
            <ul>
                <!-- Add more activity items -->
            </ul>
        </section>

        <section class="quick-actions">
            <h2>Quick Actions</h2>
            <a href="#" class="button">Add New Stock</a>
            <a href="#" class="button">Run Analysis</a>
            <a href="#" class="button">View Reports</a>
        </section>
    </div>
</div>
{% endblock %}
index.html
{% extends "base.html" %}

{% block content %}
<div class="landing-container">
    <h1 class="main-title">Welcome to Stock Portfolio Analyzer</h1>
    <p class="subtitle">Intelligent insights for smarter investments</p>
    
    {% if current_user.is_authenticated %}
        <p class="welcome-message">Hello, {{ current_user.username }}!</p>
        <a href="{{ url_for('main.profile') }}" class="cta-button">Go to Your Profile</a>
    {% else %}
        <div class="cta-container">
            <a href="{{ url_for('auth.login') }}" class="cta-button">Login</a>
            <a href="{{ url_for('auth.register') }}" class="cta-button secondary">Register</a>
        </div>
    {% endif %}
</div>
{% endblock %}
investment_survey.html
{% extends "base.html" %}

{% block content %}
<div class="survey-container">
    <h1>Investment Profile Survey</h1>
    <p class="survey-description">Help us understand your investment goals and preferences to provide personalized recommendations.</p>
    
    <form method="POST" id="investment-survey-form">
        <section class="form-section">
            <h2>Personal Information</h2>
            <div class="form-group">
                <label for="age">Age</label>
                <input type="number" name="age" id="age" min="18" max="120" required>
            </div>
            <div class="form-group">
                <label for="country">Country</label>
                <select name="country" id="country" required>
                    <option value="">Select a country</option>
                    <option value="FR">France</option>
                    <option value="DE">Germany</option>
                    <option value="IT">Italy</option>
                    <option value="ES">Spain</option>
                    <option value="UK">United Kingdom</option>
                    <!-- Add more European countries as needed -->
                </select>
            </div>
            <div class="form-group">
                <label for="education_level">Education Level</label>
                <select name="education_level" id="education_level" required>
                    <option value="">Select education level</option>
                    <option value="high_school">High School</option>
                    <option value="bachelor">Bachelor's Degree</option>
                    <option value="master">Master's Degree</option>
                    <option value="phd">PhD</option>
                </select>
            </div>
        </section>

        <section class="form-section">
            <h2>Financial Information</h2>
            <div class="form-group">
                <label for="annual_income">Annual Income (€)</label>
                <input type="number" name="annual_income" id="annual_income" min="0" step="1000" required>
            </div>
            <div class="form-group">
                <label for="monthly_investment">Monthly Investment (€)</label>
                <input type="number" name="monthly_investment" id="monthly_investment" min="0" step="100" required>
            </div>
            <div class="form-group">
                <label for="net_worth">Net Worth (€)</label>
                <input type="number" name="net_worth" id="net_worth" min="0" step="1000" required>
            </div>
        </section>

        <section class="form-section">
            <h2>Investment Preferences</h2>
            <div class="form-group">
                <label for="risk_tolerance">Risk Tolerance</label>
                <div class="slider-container">
                    <input type="range" name="risk_tolerance" id="risk_tolerance" min="1" max="5" step="1" required>
                    <div class="slider-labels">
                        <span>Low Risk</span>
                        <span>High Risk</span>
                    </div>
                </div>
            </div>
            <div class="form-group">
                <label>Investment Horizon</label>
                <div class="radio-group">
                    <input type="radio" id="short_term" name="investment_horizon" value="short_term" required>
                    <label for="short_term">Short Term (0-2 years)</label>
                    <input type="radio" id="medium_term" name="investment_horizon" value="medium_term">
                    <label for="medium_term">Medium Term (2-5 years)</label>
                    <input type="radio" id="long_term" name="investment_horizon" value="long_term">
                    <label for="long_term">Long Term (5+ years)</label>
                </div>
            </div>
            <div class="form-group">
                <label>Preferred Industries</label>
                <div class="industry-bubbles">
                    <input type="checkbox" id="tech" name="preferred_industries" value="tech">
                    <label for="tech" class="bubble">Technology</label>
                    <input type="checkbox" id="finance" name="preferred_industries" value="finance">
                    <label for="finance" class="bubble">Finance</label>
                    <input type="checkbox" id="healthcare" name="preferred_industries" value="healthcare">
                    <label for="healthcare" class="bubble">Healthcare</label>
                    <input type="checkbox" id="energy" name="preferred_industries" value="energy">
                    <label for="energy" class="bubble">Energy</label>
                    <input type="checkbox" id="consumer" name="preferred_industries" value="consumer">
                    <label for="consumer" class="bubble">Consumer Goods</label>
                    <!-- Add more industries as needed -->
                </div>
            </div>
        </section>

        <section class="form-section">
            <h2>Investment Experience</h2>
            <div class="form-group">
                <label>Have you invested before?</label>
                <div class="radio-group">
                    <input type="radio" id="experience_yes" name="investment_experience" value="yes" required>
                    <label for="experience_yes">Yes</label>
                    <input type="radio" id="experience_no" name="investment_experience" value="no">
                    <label for="experience_no">No</label>
                </div>
            </div>
            <div class="form-group" id="experience_details" style="display: none;">
                <label for="years_investing">Years of Investing Experience</label>
                <input type="number" name="years_investing" id="years_investing" min="0" max="70">
            </div>
        </section>

        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</div>

<script>
document.getElementById('experience_yes').addEventListener('change', function() {
    document.getElementById('experience_details').style.display = this.checked ? 'block' : 'none';
});
document.getElementById('experience_no').addEventListener('change', function() {
    document.getElementById('experience_details').style.display = 'none';
});
</script>
{% endblock %}
login.html
{% extends "base.html" %}

{% block content %}
<div class="auth-container">
    <h2>Login</h2>
    <form method="POST" action="{{ url_for('auth.login') }}">
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" name="email" id="email" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" name="password" id="password" required>
        </div>
        <div class="form-group">
            <label for="remember">
                <input type="checkbox" name="remember" id="remember"> Remember me
            </label>
        </div>
        <button type="submit" class="cta-button">Login</button>
    </form>
    <p>Don't have an account? <a href="{{ url_for('auth.register') }}">Register here</a></p>
</div>
{% endblock %}
portfolio.html
{% extends "base.html" %}

{% block content %}
<h1>Your Portfolios</h1>

<form action="{{ url_for('portfolio.create_portfolio') }}" method="post">
    <input type="text" name="name" placeholder="New Portfolio Name" required>
    <button type="submit">Create Portfolio</button>
</form>

{% for portfolio in portfolios %}
<div class="portfolio-summary">
    <h2>{{ portfolio.name }}</h2>
    <p>Total Value: ${{ "%.2f"|format(portfolio.total_value) }}</p>
    <p>Total Gain/Loss: ${{ "%.2f"|format(portfolio.total_gain_loss) }}</p>
    <a href="{{ url_for('portfolio.portfolio_detail', portfolio_id=portfolio.id) }}">View Details</a>
</div>
{% endfor %}
{% endblock %}
portfolio_detail.html
{% extends "base.html" %}

{% block content %}
<h1>{{ portfolio.name }}</h1>

<div class="portfolio-stats">
    <p>Total Value: ${{ "%.2f"|format(stats.total_value) }}</p>
    <p>Total Cost: ${{ "%.2f"|format(stats.total_cost) }}</p>
    <p>Total Gain/Loss: ${{ "%.2f"|format(stats.total_gain_loss) }} ({{ "%.2f"|format(stats.total_gain_loss_percentage) }}%)</p>
    <p>Number of Positions: {{ stats.num_positions }}</p>
</div>

<h2>Stocks</h2>
<table>
    <thead>
        <tr>
            <th>Ticker</th>
            <th>Company Name</th>
            <th>Shares</th>
            <th>Purchase Price</th>
            <th>Current Price</th>
            <th>Current Value</th>
            <th>Gain/Loss</th>
            <th>Gain/Loss %</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
        {% for stock in portfolio.stocks %}
        <tr>
            <td>{{ stock.ticker }}</td>
            <td>{{ stock.company_name }}</td>
            <td>{{ stock.shares }}</td>
            <td>${{ "%.2f"|format(stock.purchase_price) }}</td>
            <td>${{ "%.2f"|format(stock.current_price) }}</td>
            <td>${{ "%.2f"|format(stock.current_value) }}</td>
            <td>${{ "%.2f"|format(stock.gain_loss) }}</td>
            <td>{{ "%.2f"|format(stock.gain_loss_percentage) }}%</td>
            <td>
                <form action="{{ url_for('portfolio.sell_stock', portfolio_id=portfolio.id) }}" method="post">
                    <input type="hidden" name="stock_id" value="{{ stock.id }}">
                    <input type="number" name="shares" min="0.01" max="{{ stock.shares }}" step="0.01" required>
                    <button type="submit">Sell</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>

<h2>Add Stock</h2>
<form action="{{ url_for('portfolio.add_stock', portfolio_id=portfolio.id) }}" method="post">
    <input type="text" name="ticker" placeholder="Stock Ticker" required>
    <input type="number" name="shares" min="0.01" step="0.01" placeholder="Number of Shares" required>
    <button type="submit">Add Stock</button>
</form>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/portfolio.js') }}"></script>
{% endblock %}


profile.html
{% extends "base.html" %}

{% block content %}
<div class="profile-container">
    <h1>{{ user.username }}'s Profile</h1>
    
    <div class="profile-grid">
        <div class="profile-card account-info">
            <h2>Account Information</h2>
            <div class="info-item">
                <span class="label">Username</span>
                <span class="value">{{ user.username }}</span>
            </div>
            <div class="info-item">
                <span class="label">Email</span>
                <span class="value">{{ user.email }}</span>
            </div>
            <a href="{{ url_for('main.update_profile') }}" class="btn btn-primary">Edit Account</a>
        </div>

        {% if user.investment_profile %}
        <div class="profile-card investment-profile">
            <h2>Investment Profile</h2>
            <div class="info-item">
                <span class="label">Risk Tolerance</span>
                <span class="value">{{ user.investment_profile.risk_tolerance }}/5</span>
            </div>
            <div class="info-item">
                <span class="label">Annual Income</span>
                <span class="value">€{{ "{:,.0f}".format(user.investment_profile.annual_income) }}</span>
            </div>
            <div class="info-item">
                <span class="label">Monthly Investment</span>
                <span class="value">€{{ "{:,.0f}".format(user.investment_profile.monthly_investment) }}</span>
            </div>
            <div class="info-item">
                <span class="label">Net Worth</span>
                <span class="value">€{{ "{:,.0f}".format(user.investment_profile.net_worth) }}</span>
            </div>
            <div class="info-item">
                <span class="label">Age</span>
                <span class="value">{{ user.investment_profile.age }}</span>
            </div>
            <div class="info-item">
                <span class="label">Education</span>
                <span class="value">{{ user.investment_profile.education_level|replace('_', ' ')|title }}</span>
            </div>
            <div class="info-item">
                <span class="label">Country</span>
                <span class="value">{{ user.investment_profile.country }}</span>
            </div>
            <div class="info-item">
                <span class="label">Investment Horizon</span>
                <span class="value">{{ user.investment_profile.investment_horizon|replace('_', ' ')|title }}</span>
            </div>
            <div class="info-item">
                <span class="label">Experience</span>
                <span class="value">{{ 'Yes' if user.investment_profile.investment_experience == 'yes' else 'No' }}</span>
            </div>
            {% if user.investment_profile.investment_experience == 'yes' %}
            <div class="info-item">
                <span class="label">Years Investing</span>
                <span class="value">{{ user.investment_profile.years_investing }}</span>
            </div>
            {% endif %}
            <div class="info-item">
                <span class="label">Preferred Industries</span>
                <span class="value">{{ user.investment_profile.preferred_industries|replace(',', ', ') }}</span>
            </div>
            <div class="info-item">
                <span class="label">Last Updated</span>
                <span class="value">{{ user.investment_profile.last_updated.strftime('%Y-%m-%d %H:%M') }}</span>
            </div>
            <a href="{{ url_for('main.investment_survey') }}" class="btn btn-primary">Update Profile</a>
        </div>
        {% else %}
        <div class="profile-card investment-profile">
            <h2>Investment Profile</h2>
            <p>You haven't completed the investment profile survey yet.</p>
            <a href="{{ url_for('main.investment_survey') }}" class="btn btn-primary">Complete Survey</a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
register.html
{% extends "base.html" %}

{% block content %}
<div class="auth-container">
    <h2>Register</h2>
    <form method="POST" action="{{ url_for('auth.register') }}">
        <div class="form-group">
            <label for="email">Email</label>
            <input type="email" name="email" id="email" required>
        </div>
        <div class="form-group">
            <label for="username">Username</label>
            <input type="text" name="username" id="username" required>
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" name="password" id="password" required>
        </div>
        <div class="form-group">
            <label for="confirmation">Confirm Password</label>
            <input type="password" name="confirmation" id="confirmation" required>
        </div>
        <button type="submit" class="cta-button">Register</button>
    </form>
    <p>Already have an account? <a href="{{ url_for('auth.login') }}">Login here</a></p>
</div>
{% endblock %}