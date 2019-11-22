from flask import (
    Blueprint,
)

from flask_restplus import Resource


main = Blueprint('bpi', __name__)


class Todo(Resource):
    def get(self):
        return {'bpi': 'bpi'}
