import bcrypt
import datetime
import jwt

from sqlalchemy import Column, BigInteger, Numeric, DateTime, Text, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship

from app import db, app


class ModelWithTimestamps:
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())


class Role(db.Model, ModelWithTimestamps):
    __tablename__ = 'roles'

    ROLE_REGULAR = 'regular'
    ROLE_ADMIN = 'admin'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    def is_admin_role(self):
        return self.name == self.ROLE_ADMIN

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }


class User(db.Model, ModelWithTimestamps):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    login = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    role_id = Column(BigInteger, ForeignKey(Role.id), nullable=False)

    role = relationship(Role, backref='users')

    def is_admin(self):
        return self.role.is_admin_role()

    def get_account_by_currency(self, currency):
        account = list(filter(lambda x: x.currency == currency, self.accounts))

        if len(account):
            return account[0]

        return None

    def hash_and_save_password(self, password):
        self.password = User.hash_password(password)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def validate_user_password(self, password):
        return bcrypt.checkpw(
            password.encode(),
            self.password.encode()
        )

    @classmethod
    def find_by_login(cls, login):
        return cls.query.filter_by(login=login).first()

    def to_json(self):
        return {
            'id': self.id,
            'login': self.login,
            'role': self.role.to_json(),
            'accounts': [account.to_json() for account in self.accounts]
        }

    def encode_auth_token(self):
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['TOKEN_EXPIRE_HOURS'])

        return jwt.encode({'login': self.login, 'exp': exp}, app.config['SECRET_KEY'], algorithm='HS256')

    def is_account_owner(self, account):
        return self.id == account.user_id


class Currency(db.Model, ModelWithTimestamps):
    __tablename__ = 'currencies'

    id = Column(BigInteger, primary_key=True)
    ticker = Column(Text, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'ticker': self.ticker
        }


class CurrencyRate(db.Model, ModelWithTimestamps):
    __tablename__ = 'currency_rates'

    currency_from_id = Column(BigInteger, ForeignKey(Currency.id), nullable=False, primary_key=True)
    currency_to_id = Column(BigInteger, ForeignKey(Currency.id), nullable=False, primary_key=True)
    value = Column(Numeric, nullable=False)

    currency_from = relationship(Currency, foreign_keys=[currency_from_id])
    currency_to = relationship(Currency, foreign_keys=[currency_to_id])


class Fee(db.Model, ModelWithTimestamps):
    __tablename__ = 'fees'

    TYPE_INTERNAL_TRANSFER = 100
    TYPE_EXTERNAL_TRANSFER = 200

    id = Column(BigInteger, primary_key=True)
    type = Column(BigInteger, nullable=False, unique=True)
    percent = Column(Numeric, nullable=False, server_default='0')


class Account(db.Model, ModelWithTimestamps):
    __tablename__ = 'accounts'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    balance = Column(Numeric, nullable=False, server_default='0')
    currency_id = Column(BigInteger, ForeignKey(Currency.id), nullable=False)

    user = relationship(User, backref='accounts')
    currency = relationship(Currency, backref='accounts')

    def is_owner(self, user):
        return user.id == self.user_id

    def has_enough_funds(self, value):
        return self.balance >= value

    def to_json(self, private=False):
        data = {
            'id': self.id,
            'currency': self.currency.to_json(),
            'user': self.user.login
        }

        if private:
            data['balance'] = float(self.balance)

        return data


class Event(db.Model, ModelWithTimestamps):
    __tablename__ = 'events'

    STATUS_PENDING = 200
    STATUS_SUCCESS = 300
    STATUS_FAILED = 300

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    status = Column(BigInteger, nullable=False, default=STATUS_PENDING, server_default=str(STATUS_PENDING))

    user = relationship(User, backref='events')

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'transactions': [transaction.to_json() for transaction in self.transactions],
            'created_at': datetime.datetime.timestamp(self.created_at)
        }


class Transaction(db.Model, ModelWithTimestamps):
    __tablename__ = 'transactions'

    TYPE_TRANSFER = 100
    TYPE_FEE = 200
    TYPE_CONVERT = 300

    id = Column(BigInteger, primary_key=True)
    value = Column(Numeric, nullable=False)
    type = Column(BigInteger, nullable=False)
    event_id = Column(BigInteger, ForeignKey(Event.id), nullable=False)
    account_from_id = Column(BigInteger, ForeignKey(Account.id), nullable=False)
    account_to_id = Column(BigInteger, ForeignKey(Account.id), nullable=False)

    event = relationship(Event, backref='transactions')
    account_from = relationship(Account, foreign_keys=[account_from_id])
    account_to = relationship(Account, foreign_keys=[account_to_id])

    def to_json(self):
        return {
            'id': self.id,
            'account_from': self.account_from.to_json(),
            'account_to': self.account_to.to_json(),
            'value': float(self.value),
            'type': self.type
        }
