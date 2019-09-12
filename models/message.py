from sqlalchemy import Column, Unicode, UnicodeText, Integer

from models.base_model import SQLMixin, db
from models.user import User
from models import mailer

from config import admin_mail


def send_mail(subject, author, to, content):
    m = mailer.new(
        subject=subject,
        author=author,
        to=to,
    )
    m.plain = content
    mailer.send(m)


class Message(SQLMixin, db.Model):

    __tablename__ = 'messages'

    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)

    @staticmethod
    def send(title: str, content: str, sender_id: int, receiver_id: int):
        form = dict(
            title=title,
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id
        )
        Message.new(form)

        receiver: User = User.one(id=receiver_id)

        send_mail(
            subject=title,
            author=admin_mail,
            to=receiver.email,
            content='站内信通知：\n {}'.format(content),
        )

    def sender(self):
        u = User.one(id=self.sender_id)
        return u

    def receiver(self):
        u = User.one(id=self.receiver_id)
        return u
