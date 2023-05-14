"""
@FileName：decorators.py
@Author：stone
@Time：2023/5/13 20:59
@Description:装饰器
"""

from functools import wraps
from flask_login import current_user
from flask import Markup, url_for, flash, redirect


def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                '请先确认账户',
                '没有接收到邮件',
                '<a class="alert-link" href="%s">确认邮件</a>' % url_for('auth.resend_confirm')
            )
            flash(message, 'warning')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)

    return decorated_function
