from functools import wraps

import jwt
from flask import request, abort, g

from app import app
from models import User


def login_required(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        header = request.headers.get('Authorization')
        _, token = header.split()
        decoded = {}

        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except jwt.DecodeError:
            abort(400, message='Token is not valid.')
        except jwt.ExpiredSignatureError:
            abort(400, message='Token is expired.')

        login = decoded['login']
        user = User.find_by_login(login)

        if not user:
            abort(400, message='User not found.')

        g.current_user = user

        return method(*args, **kwargs)

    return wrapper
