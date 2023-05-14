# -*- coding: utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,AnonymousUserMixin
from flask_wtf import CSRFProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
csrf =  CSRFProtect()



@login_manager.user_loader
def load_user(user_id):
    from albumy.models import User
    user = User.query.get(int(user_id))
    return user


class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

    def  can(self,permission_name):
        return False


login_manager.anonymous_user =Guest
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
