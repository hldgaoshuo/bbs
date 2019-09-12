import logging

import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from werkzeug.datastructures import FileStorage

from models.user import User

from routes import current_user


main = Blueprint('setting', __name__)


@main.route('/setting')
def setting():
    u = current_user()
    if u is None:
        return redirect(url_for('login.login'))
    else:
        return render_template(
            'setting.html',
            user=u,
        )


@main.route('/username/update', methods=['POST'])
def update_username():
    u = current_user()

    new_name = request.form.get('username', '')
    if new_name != '':
        User.update(u.id, username=new_name)

    return redirect(url_for('profile.profile'))


@main.route('/signature/update', methods=['POST'])
def update_signature():
    u = current_user()

    signature = request.form.get('signature', '')
    if signature != '':
        User.update(u.id, signature=signature)

    return redirect(url_for('profile.profile'))


@main.route('/password/update', methods=['POST'])
def update_password():
    u = current_user()
    old_pass = request.form.get('old_pass', '')
    logging.debug("type of old_pass: {}".format(type(old_pass)))
    logging.debug("update_password, old password: {}".format(old_pass))
    new_pass = request.form.get('new_pass', '')
    logging.debug("update_password, new password: {}".format(new_pass))

    logging.debug("update_password, input salted password: {}".format(User.salted_password(old_pass)))
    logging.debug("update_password, old salted password: {}".format(u.password))
    if User.salted_password(old_pass) == u.password:
        u.update(id=u.id, password=User.salted_password(new_pass))
        return redirect(url_for('login.login'))
    else:
        abort(401)


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    filename = str(uuid.uuid4())
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('profile.profile'))
