from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class TransactionForm(Form):
    customer_phone = StringField('Customer_phone', validators=[DataRequired(), Length(min=9, max=10, message='Customer Phone number invalid')])
    employee_phone = StringField('Employee_phone', validators=[DataRequired(), Length(min=9, max=10, message='Employee Phone number invalid')])
    product_id = StringField('Product_id', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])

class RegisterForm(Form):
    name = StringField('Username', validators=[DataRequired(), Length(min=6, max=25, message='Name must be in range 6 - 25')])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, max=10, message='Phone number is not valid')])
    address = StringField('Address', validators=[Length(min=6, max=128)])
    confirm = StringField('Repeat Address', [EqualTo('Address', message='Address must match')])


class LoginForm(Form):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    phone = StringField('phone', validators=[DataRequired(), Length(min=9, max=10, message='Phone number is not valid')])
