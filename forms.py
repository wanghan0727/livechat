from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, email_validator
from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    pasw_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='密碼需要吻合')])
    submit = SubmitField('Register')

    def check_email(self, field):
        # """檢查Email"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('電子郵件已經被註冊過了')
    
    def check_username(self, field):
        # """檢查username"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('使用者名稱已經存在')