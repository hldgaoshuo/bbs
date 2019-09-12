from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.message import Message


main = Blueprint('message', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    u = current_user()
    receiver_name = form['receivername']
    receiver = User.one(username=receiver_name)
    Message.send(
        title=form['title'],
        content=form['content'],
        sender_id=u.id,
        receiver_id=receiver.id
    )
    return redirect(url_for('message.index'))


@main.route('/')
def index():
    u = current_user()
    if u is None:
        return redirect(url_for('login.login'))
    else:
        send = Message.all(sender_id=u.id)
        received = Message.all(receiver_id=u.id)
        return render_template(
            'message/index.html',
            user=u,
            send=send,
            received=received,
        )


@main.route('/view/<int:id>')
def view(id):
    message = Message.one(id=id)
    u = current_user()
    if u.id in [message.receiver_id, message.sender_id]:
        return render_template('message/detail.html', message=message, user=u)
    else:
        return redirect(url_for('message.index'))
