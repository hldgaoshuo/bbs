from flask import (
    Blueprint,
)


main = Blueprint('logout', __name__)


@main.route("/logout")
def logout():
    pass
