from sqlalchemy import Unicode, Column

from models.base_model import db, SQLMixin


class Board(SQLMixin, db.Model):

    __tablename__ = 'board'

    title = Column(Unicode(50), nullable=False)
