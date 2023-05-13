"""
@FileName：auth.py
@Author：stone
@Time：2023/5/13 20:56
@Description:
"""

from flask import Blueprint, url_for, flash, redirect, render_template
from flask_login import current_user,login_user

from albumy.forms.auth import RegisterForm, LoginForm
from albumy.models import User
from albumy.extensions import db
from albumy.settings import Operations
from albumy.utils import generate_token, redirect_back
from albumy.emails import send_confirm_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return (url_for('main.index'))

    form = RegisterForm()
    if form.validate_email():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(name=name, email=email, username=username)
        user.set_password(password)
        db.session(user)
        db.session.commit()
        # 生成token
        token = generate_token(user=user, operation='confirm')
        send_confirm_email(user=user, token=token)
        flash("确认发送邮件,点击按钮", 'info')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mian.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("登录成功", 'info')
            return redirect_back()
        flash("邮箱或者密码无效", 'warning')
    return render_template('auth/login.html', form=form)
