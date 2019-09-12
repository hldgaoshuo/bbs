import config

import hashlib

from sqlalchemy import Column, String

from models.base_model import SQLMixin, db


class User(SQLMixin, db.Model):

    __tablename__ = 'user'

    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    signature = Column(String(100), nullable=False, default='无签名')
    image = Column(String(100), nullable=False, default='/images/default.png')
    email = Column(String(50), nullable=False, default=config.test_mail)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        username = form.get('username', '')
        if len(username) > 2 and User.one(username=username) is None:
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )

        u = User.one(**query)

        return u
