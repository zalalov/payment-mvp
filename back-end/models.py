from sqlalchemy import Column, BigInteger, Numeric, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import relationship

from app import db
from exceptions import InvalidModelProperties


class ModelWithTimestamps:
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())


class Role(db.Model, ModelWithTimestamps):
    __tablename__ = 'roles'

    ROLE_REGULAR = 100
    ROLE_ADMIN = 666

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class User(db.Model, ModelWithTimestamps):
    __tablename__ = 'users'

    GENDER_MALE = 10
    GENDER_FEMAIL = 20
    GENDER_OTHER = 30
    GENDER_NONE = 40

    id = Column(BigInteger, primary_key=True)
    login = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    role_id = Column(BigInteger, ForeignKey(Role.id), nullable=False)

    role = relationship(Role, backref='users')

    def __init__(self, login, password, salt, role_id):
        self.login = login
        self.password = password
        self.salt = salt
        self.role_id = role_id


class Currency(db.Model, ModelWithTimestamps):
    __tablename__ = 'currencies'

    id = Column(BigInteger, primary_key=True)
    ticker = Column(Text, nullable=False)

    def __init__(self, ticker):
        self.ticker = ticker


class CurrencyRate(db.Model, ModelWithTimestamps):
    __tablename__ = 'currency_rates'

    currency_from_id = Column(BigInteger, ForeignKey(Currency.id), nullable=False, primary_key=True)
    currency_to_id = Column(BigInteger, ForeignKey(Currency.id), nullable=False, primary_key=True)
    value = Column(Numeric, nullable=False)

    currency_from = relationship(Currency, foreign_keys=[currency_from_id])
    currency_to = relationship(Currency, foreign_keys=[currency_to_id])

    def __init__(self, currency_from_id, currency_to_id):
        self.currency_from_id = currency_from_id
        self.currency_to_id = currency_to_id


class Fee(db.Model, ModelWithTimestamps):
    __tablename__ = 'fees'

    TYPE_INTERNAL_TRANSFER = 100
    TYPE_EXTERNAL_TRANSFER = 200

    id = Column(BigInteger, primary_key=True)
    type = Column(BigInteger, nullable=False, unique=True)
    percent = Column(Numeric, nullable=False, server_default='0')


class Account(db.Model, ModelWithTimestamps):
    __tablename__ = 'accounts'

    TYPE_USD = 1000
    TYPE_EUR = 2000
    TYPE_CNY = 3000

    AVAILABLE_TYPES = [
        TYPE_USD,
        TYPE_EUR,
        TYPE_CNY
    ]

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    balance = Column(Numeric, nullable=False, server_default='0')
    currency_id = Column(BigInteger, ForeignKey(Currency.id), nullable=False)

    user = relationship(User, backref='accounts')
    currency = relationship(Currency, backref='accounts')

    def __init__(self, user_id, type, balance):
        if type not in self.AVAILABLE_TYPES:
            raise InvalidModelProperties()

        self.user_id = user_id
        self.balance = balance


class Event(db.Model, ModelWithTimestamps):
    __tablename__ = 'events'

    id = Column(BigInteger, primary_key=True)
    type = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, ForeignKey(User.id), nullable=False)
    account_from_id = Column(BigInteger, ForeignKey(Account.id), nullable=False)
    account_to_id = Column(BigInteger, ForeignKey(Account.id), nullable=False)

    user = relationship(User, backref='events')
    account_from = relationship(Account, foreign_keys=[account_from_id])
    account_to = relationship(Account, foreign_keys=[account_to_id])

    def __init__(self, type, user_id, account_from_id, account_to_id):
        self.type = type
        self.user_id = user_id
        self.account_from_id = account_from_id
        self.account_to_id = account_to_id


class Transaction(db.Model, ModelWithTimestamps):
    __tablename__ = 'transactions'

    id = Column(BigInteger, primary_key=True)
    value = Column(Numeric, nullable=False)
    event_id = Column(BigInteger, ForeignKey(Event.id), nullable=False)

    event = relationship(Event, backref='event')

    def __init__(self, value, event_id):
        self.value = value
        self.event_id = event_id
