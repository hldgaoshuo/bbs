from flask import (
    Blueprint,
)

from flask_restplus import Resource


main = Blueprint('api', __name__)


class TodoItem(Resource):
    def get(self):
        return {'hello': 'world'}
