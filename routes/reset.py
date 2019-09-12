import uuid

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from models.message import Message
from models.user import User

from routes import cache, new_csrf_token


main = Blueprint('reset', __name__)


@main.route("/index")
def index():
    return render_template('reset/index.html')


@main.route("/send", methods=['POST'])
def send():
    username = request.form.get('username', '')
    user = User.one(username=username)

    token = str(uuid.uuid4())
    k = 'csrf_tokens_{}'.format(token)
    v = user.id
    cache.set(k, v)

    title = 'reset password'
    content = 'http://localhost:3000/reset/view?token=' + token
    sender_id = 100
    receiver_id = user.id
    Message.send(title, content, sender_id, receiver_id)

    return redirect(url_for('login.login'))


@main.route("/view")
def view():
    token = request.args.get('token', '')
    k = 'csrf_tokens_{}'.format(token)

    if not cache.exists(k):
        abort(401)

    return render_template('reset/view.html', token=token)


@main.route("/update/<string:token>", methods=['POST'])
def update(token):
    k = 'csrf_tokens_{}'.format(token)
    v = cache.get(k)
    uid = v
    if uid is None:
        abort(401)

    u = User.one(id=uid)
    new_pass = request.form['password']
    u.update(id=u.id, password=User.salted_password(new_pass))

    return redirect(url_for('login.login'))
