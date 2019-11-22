from flask import (
    Blueprint,
)

from flask_restplus import Resource


main = Blueprint('hello', __name__)


class Hello(Resource):
    def get(self):
        return {'hello': 'world'}
