import bcrypt

from app import db
from exceptions import InvalidDBSchemeStateException
from models import User, Account, Currency, Role


def create_user(login, password, role_id=None):
    user = db.session.query(User).filter(User.login == login).first()

    if user:
        return

    user = User()
    user.login = login
    user.hash_and_save_password(password)

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
