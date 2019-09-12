import logging

from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.base_model import db
from models.topic import Topic
from models.topic import Reply
from models.board import Board


main = Blueprint('topic', __name__)


@main.route("/")
def index():
    user = current_user()

    board_id = request.args.get('board_id')
    if board_id is None:
        board_id = 1
    if board_id == '':
        board_id = 1

    if board_id == 1:
        topics = Topic.all()
    else:
        topics = Topic.all(board_id=board_id)
    boards = Board.all()
    return render_template("topic/index.html", user=user, topics=topics, boards=boards, board_id=board_id)


@main.route('/<int:id>')
def detail(id):
    token = new_csrf_token()
    topic = Topic.get(id)
    return render_template("topic/detail.html", token=token, topic=topic)


@main.route("/new")
def new():
    board_id = request.args.get('board_id')
    if board_id == '':
        board_id = '1'

    boards = Board.all()
    token = new_csrf_token()
    return render_template("topic/new.html", boards=boards, token=token, board_id=board_id)


@main.route("/delete")
@csrf_required
def delete():
    topic_id = int(request.args.get('id'))
    Topic.query.filter_by(id=topic_id).delete()
    Reply.query.filter_by(topic_id=topic_id).delete()
    db.session.commit()
    return redirect(url_for('topic.index'))


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('topic.index'))
