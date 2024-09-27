from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class VMProvisionForm(FlaskForm):
    name = StringField('VM Name', validators=[DataRequired(), Length(min=1, max=64)])
    cpu_cores = IntegerField('CPU Cores', validators=[DataRequired(), NumberRange(min=1, max=32)])
    ram = IntegerField('RAM (GB)', validators=[DataRequired(), NumberRange(min=1, max=128)])
    disk_size = IntegerField('Disk Size (GB)', validators=[DataRequired(), NumberRange(min=10, max=1000)])
    os_image = SelectField('OS Image', choices=[('ubuntu', 'Ubuntu'), ('windows', 'Windows')], validators=[DataRequired()])
    submit = SubmitField('Provision VM')

class BillingForm(FlaskForm):
    amount = DecimalField('Amount (in Naira)', validators=[DataRequired(), NumberRange(min=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Pay Now')
