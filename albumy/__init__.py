# -*- coding: utf-8 -*-

import os

import click
from flask import Flask, render_template

from albumy.blueprints.main import main_bp
from albumy.blueprints.auth import auth_bp
from albumy.blueprints.user import user_bp

from albumy.extensions import bootstrap, db, mail, moment, login_manager, csrf, dropzone, avatars
from albumy.fakes import fake_photo
from albumy.models import User, Role
from albumy.settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('albumy')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errorhandlers(app)
    register_shell_context(app)
    register_template_context(app)

    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    dropzone.init_app(app)
    avatars.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)


def register_template_context(app):
    pass


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def init():
        """Initialize Albumy."""
        click.echo('Initializing the database...')
        db.create_all()

        click.echo('Done.')

    @app.cli.command()
    @click.option('--user', default=10, help="创建用户,默认为10个")
    @click.option('--photo', default=50, help="创建照片,默认为50个")
    def forge(user,photo):
        """Generate fake data."""
        from albumy.fakes import fake_admin, fake_user
        db.drop_all()
        db.create_all()

        click.echo("初始化角色和权限")
        Role.init_role()
        click.echo("创建管理员用户")
        fake_admin()
        click.echo("生成 %d 个用户" % user)
        fake_user(user)
        click.echo("生成 %d 张照片"%photo)
        fake_photo(photo)
        click.echo('完成')
