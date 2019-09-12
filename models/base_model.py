from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer

from models import current_time


db = SQLAlchemy()


class SQLMixin(object):

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_time = Column(Integer, default=current_time)
    updated_time = Column(Integer, default=current_time)

    @classmethod
    def new(cls, form):
        m = cls()
        for name, value in form.items():
            setattr(m, name, value)

        db.session.add(m)
        db.session.commit()

        return m

    @classmethod
    def all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()

        return ms

    @classmethod
    def one(cls, **kwargs):
        m = cls.query.filter_by(**kwargs).first()

        return m

    @classmethod
    def update(cls, id, **kwargs):
        m = cls.query.filter_by(id=id).first()
        for name, value in kwargs.items():
            setattr(m, name, value)

        db.session.add(m)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
