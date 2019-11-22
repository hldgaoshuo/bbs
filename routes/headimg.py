from flask import (
    Blueprint,
)

from flask_restplus import Resource


main = Blueprint('headimg', __name__)


class HeadImg(Resource):
    def get(self):
        return {'headimg': 'baidu.com'}
