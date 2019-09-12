from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
)

from models.reply import Reply
from models.topic import Topic

from routes import current_user


main = Blueprint('profile', __name__)


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


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('login.login'))
    else:
        created = created_topic(u.id)
        replied = replied_topic(u.id)
        return render_template(
            'profile.html',
            user=u,
            created=created,
            replied=replied
        )
