import uuid
import redis

import config

from functools import wraps

from flask import session, request, abort

from models.user import User


cache = redis.StrictRedis(host=config.cache_host, port=config.cache_port)


def current_user():
    session_id = session.get('session_id', '')
    k = 'sessions_{}'.format(session_id)
    v = cache.get(k)
    uid = v
    u: User = User.one(id=uid)
    return u


def new_csrf_token():
    token = str(uuid.uuid4())
    k = 'csrf_tokens_{}'.format(token)
    user = current_user()
    if user is None:
        v = -1
    else:
        v = user.id
    cache.set(k, v)
    return token


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        k = 'csrf_tokens_{}'.format(token)
        u = current_user()
        if cache.exists(k) and int(cache.get(k)) == u.id:
            cache.delete(k)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper
