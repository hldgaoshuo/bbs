from flask import (
    render_template,
    Blueprint,
    abort,
    send_from_directory,
)

from models.user import User
from models.reply import Reply
from models.topic import Topic
from models.board import Board

from routes import current_user

from log import logger


main = Blueprint('index', __name__)


"""
用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    # logger.info('index')
    u = current_user()
    ts = Topic.all()
    bs = Board.all()
    return render_template('index.html', user=u, topics=ts, boards=bs)


def created_topic(user_id):
    ts = Topic.all(user_id=user_id)
    return ts


def replied_topic(user_id):
    rs = Reply.all(user_id=user_id)
    ts = []
    for r in rs:
        t = Topic.one(id=r.topic_id)
        ts.append(t)
    return ts


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        created = created_topic(u.id)
        replied = replied_topic(u.id)
        return render_template(
            'profile.html',
            user=u,
            created=created,
            replied=replied
        )


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)
