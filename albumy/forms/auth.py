"""
@FileName：auth.py
@Author：stone
@Time：2023/5/13 20:56
@Description:
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from albumy.models import User


class RegisterForm(FlaskForm):
    """住粗表单"""
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField("Username", validators=[DataRequired(), Length(1, 20),
                                                   Regexp('^[a-zA-Z0-9]*$', message="输入的用户名中只包含英文字母和数字")])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("此邮件已经注册过了")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("此用户名已经注册过了")


class LoginForm(FlaskForm):
    """登录表单"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField()


class ForgetPasswordForm(FlaskForm):
    """忘记密码"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField()


class ResetPasswordForm(FlaskForm):
    """重置密码"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()
