from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class AddStockForm(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired(), Length(min=1, max=10)])
    shares = FloatField('Number of Shares', validators=[DataRequired(), NumberRange(min=0.01)])
    purchase_price = FloatField('Purchase Price', validators=[DataRequired(), NumberRange(min=0.01)])
    purchase_date = DateField('Purchase Date', validators=[DataRequired()])
    submit = SubmitField('Add Stock')
    
    