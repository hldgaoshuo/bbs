import uuid

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
)

from models.user import User

from routes import cache


main = Blueprint('login', __name__)


@main.route("/login")
def login():
    return render_template('login.html')


@main.route("/authenticate", methods=['POST'])
def authenticate():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('login.login'))
    else:
        session_id = str(uuid.uuid4())
        k = 'sessions_{}'.format(session_id)
        v = u.id
        cache.set(k, v)
        session['session_id'] = session_id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))
