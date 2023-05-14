"""
@FileName：fakes.py
@Author：stone
@Time：2023/5/13 20:59
@Description:生成测试数据
"""
import os.path
import random

from faker import Faker
from flask import current_app
from PIL import Image
from albumy.models import User, Photo
from albumy.extensions import db
from sqlalchemy.exc import IntegrityError

fake = Faker('zh_CN')


def fake_admin():
    admin = User(
        name='Grey Li',
        username='greyli',
        email='admin@helloflask.com',
        bio=fake.sentence(),
        website='http://greyli.com',
        confirmed=True)
    admin.set_password('12345678')
    db.session.add(admin)
    db.session.commit()


def fake_user(count=10):
    for _ in range(count):
        user = User(
            name=fake.name(),
            username=fake.user_name(),
            email=fake.email(),
            bio=fake.sentence(),
            website=fake.url(),
            location=fake.city(),
            member_since=fake.date_this_decade(),
            confirmed=True
        )
        user.set_password('12345678')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_photo(count=30):
    upload_path = current_app.config['ALBUMY_UPLOAD_PATH']
    for i in range(count):
        filename = 'random_{}.jpg'.format(i)
        r = lambda: random.randint(128, 255)
        img = Image.new(mode='RGB', size=(800, 800), color=(r(), r(), r()))
        img.save(os.path.join(upload_path, filename))

        photo = Photo(
            description=fake.text(),
            filename=filename,
            filename_m=filename,
            filename_s=filename,
            author=User.query.get(random.randint(1, User.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(photo)
    db.session.commit()
