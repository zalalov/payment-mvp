import jwt

from functools import wraps
from flask import abort, request, g

from models import User, Account, Currency, Role
from exceptions import InvalidDBSchemeStateException
from app import db, app


def create_user(login, password, role_id=None):
    user = db.session.query(User).filter(User.login == login).first()

    if user:
        return

    user = User()
    user.login = login
    user.hash_password(password)

    if role_id:
        role = db.session.query(Role).get(role_id)
    else:
        role = db.session.query(Role).filter(Role.name == Role.ROLE_REGULAR).first()

    if not role:
        raise InvalidDBSchemeStateException('Invalid role.')

    user.role = role
    db.session.add(user)

    currencies = db.session.query(Currency).all()

    for currency in currencies:
        account = Account()
        account.user = user
        account.currency = currency

        if currency.ticker == 'USD':
            account.balance = 100

        db.session.add(account)

    db.session.commit()

    return user


def get_admin_account():
    return db.session.query(User).join(Role).filter(Role.name == Role.ROLE_ADMIN).one()


def login_required(method):
    @wraps(method)
    def wrapper(self):
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

        return method(self)

    return wrapper
