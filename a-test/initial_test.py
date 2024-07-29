import unittest
from app import create_app, db
from app.models import User, InvestmentProfile
from flask_login import current_user

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register_user(self, username, email, password):
        response = self.client.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=password
        ), follow_redirects=True)
        if b'Username already taken' in response.data or b'Email already registered' in response.data:
            return self.login_user(email, password)
        return response


    def login_user(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout_user(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_flask_server_runs(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_database_and_schema_creation(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        queried_user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.username, 'testuser')

    def test_user_registration_login_logout(self):
        # Test user registration
        response = self.register_user('testuser', 'test@example.com', 'password123')
        self.assertIn(b'Registration successful', response.data)

        # Test login
        response = self.login_user('test@example.com', 'password123')
        self.assertIn(b'Dashboard', response.data)

        # Test logout
        response = self.logout_user()
        self.assertIn(b'You have been logged out', response.data)

    def test_investment_survey(self):
        # Register and login a user
        self.register_user('investor', 'investor@example.com', 'password123')
        self.login_user('investor@example.com', 'password123')

        # Submit investment survey
        response = self.client.post('/investment-survey', data=dict(
            risk_tolerance='2',
            annual_income='75000',
            monthly_investment='1000',
            net_worth='250000',
            preferred_industries='Technology,Healthcare',
            age='30',
            education_level='bachelor',
            country='US',
            investment_horizon='medium',
            investment_experience='intermediate',
            years_investing='5'
        ), follow_redirects=True)

        self.assertIn(b'Investment profile updated successfully', response.data)

        # Check if the investment profile was saved correctly
        user = User.query.filter_by(email='investor@example.com').first()
        profile = user.investment_profile
        self.assertIsNotNone(profile)
        self.assertEqual(profile.risk_tolerance, '2')
        self.assertEqual(profile.annual_income, 75000)
        self.assertEqual(profile.monthly_investment, 1000)
        self.assertEqual(profile.net_worth, 250000)
        self.assertEqual(profile.preferred_industries, 'Technology,Healthcare')
        self.assertEqual(profile.age, 30)
        self.assertEqual(profile.education_level, 'bachelor')
        self.assertEqual(profile.country, 'US')
        self.assertEqual(profile.investment_horizon, 'medium')
        self.assertEqual(profile.investment_experience, 'intermediate')
        self.assertEqual(profile.years_investing, 5)

if __name__ == '__main__':
    unittest.main()