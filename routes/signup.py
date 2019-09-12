from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.user import User


main = Blueprint('signup', __name__)


@main.route("/signup")
def signup():
    return render_template('signup.html')


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    User.register(form)
    return redirect(url_for('login.login'))

