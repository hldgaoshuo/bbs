import logging

import secret
import config
import filter

from flask import Flask
from flask_restplus import Api

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from models.base_model import db
from models.user import User
from models.board import Board
from models.message import Message
from models.reply import Reply
from models.topic import Topic

from routes.index import main as index_routes
from routes.login import main as login_routes
from routes.signup import main as signup_routes
from routes.profile import main as profile_routes
from routes.reset import main as reset_routes
from routes.setting import main as setting_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.message import main as message_routes
from routes.api import main as api_routes
from routes.bpi import main as bpi_routes

from routes.api import TodoItem
from routes.bpi import Todo


def configured_app():
    app = Flask(__name__)

    app.secret_key = secret.secret_key

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4'.format(
        config.database_username,
        secret.database_password,
        config.database_ip,
        config.database,
    )

    db.init_app(app)

    api = Api(api_routes, doc='/doc/')

    register_resources(api)
    register_routes(app)
    register_filter(app)
    register_admin(app)

    return app


def register_resources(api):
    api.add_resource(TodoItem, '/todos/')
    api.add_resource(Todo, '/todoz/')


def register_routes(app):
    app.register_blueprint(index_routes)
    app.register_blueprint(login_routes)
    app.register_blueprint(signup_routes)
    app.register_blueprint(profile_routes)
    app.register_blueprint(setting_routes)
    app.register_blueprint(reset_routes, url_prefix='/reset')
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(message_routes, url_prefix='/message')
    app.register_blueprint(api_routes)
    app.register_blueprint(bpi_routes)


def register_filter(app):
    app.template_filter()(filter.count)
    app.template_filter()(filter.format_time)


def register_admin(app):
    admin = Admin(app, name='web19', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session, endpoint="user_"))
    admin.add_view(ModelView(Board, db.session, endpoint="board_"))
    admin.add_view(ModelView(Message, db.session, endpoint="message_"))
    admin.add_view(ModelView(Reply, db.session, endpoint="reply_"))
    admin.add_view(ModelView(Topic, db.session, endpoint="topic_"))


# 运行代码
if __name__ == '__main__':
    # logging.basicConfig(filename='example.log', level=logging.DEBUG)

    app = configured_app()

    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.jinja_env.auto_reload = True

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    config = dict(
        debug=True,
        host=config.server_host,
        port=config.server_port,
        threaded=True,
    )
    app.run(**config)
