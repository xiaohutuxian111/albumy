"""
@FileName：emails.py
@Author：stone
@Time：2023/5/13 21:00
@Description:邮件工具
"""

from flask_mail import Message
from threading import Thread
from flask import current_app, render_template
from albumy.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(to, subject, template, **kwargs):
    message = Message(current_app.config['ALBUMY_MAIL_SUBJECT_PREFIX'] + subject, recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


def send_confirm_email(user, token, to=None):
    """发送确认邮件"""
    send_mail(subject='确认邮件', to=to or user.email, template='emails/confirm', user=user, token=token)


def send_reset_password_email(user, token):
    send_mail(subject='重置密码', to=user.email, template='emails/reset_password', user=user, token=token)
