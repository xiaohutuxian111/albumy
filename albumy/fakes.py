"""
@FileName：fakes.py
@Author：stone
@Time：2023/5/13 20:59
@Description:生成测试数据
"""
from faker import Faker
from albumy.models import User
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



