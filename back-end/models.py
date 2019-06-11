from sqlalchemy import Column, BigInteger, Numeric, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from exceptions import InvalidModelProperties


class ModelWithTimestamps:
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())


class Role(Base, ModelWithTimestamps):
    __tablename__ = 'roles'

    ROLE_REGULAR = 100
    ROLE_ADMIN = 666

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)

    def __init__(self, name):
        self.name = name


class User(Base, ModelWithTimestamps):
    __tablename__ = 'users'

    GENDER_MALE = 10
    GENDER_FEMAIL = 20
    GENDER_OTHER = 30
    GENDER_NONE = 40

    id = Column(BigInteger, primary_key=True)
    login = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    salt = Column(Text, nullable=False)
    role_id = Column(BigInteger, ForeignKey(Role.id), nullable=False)

    role = relationship(Role, backref='users')

    def __init__(self, email, password):
        self.email = email
        self.password = password


class Account(Base, ModelWithTimestamps):
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
    balance = Column(Numeric, nullable=False, default=0)

    user = relationship(User, backref='accounts')

    def __init__(self, user_id, type, balance):
        if type not in self.AVAILABLE_TYPES:
            raise InvalidModelProperties()

        self.user_id = user_id
        self.balance = balance


class Transaction(Base, ModelWithTimestamps):
    __tablename__ = 'transactions'

    id = Column(BigInteger, primary_key=True)
    value = Column(Numeric, nullable=False)
    account_from_id = Column(BigInteger, ForeignKey(Account.id), nullable=False)
    account_to_id = Column(BigInteger, ForeignKey(Account.id), nullable=False)

    account_from = relationship(Account, backref='transactions')
    account_to = relationship(Account, backref='transactions')

    def __init__(self, value, account_from_id, account_to_id):
        self.value = value
        self.account_from_id = account_from_id
        self.account_to_id = account_to_id


class Currency(Base, ModelWithTimestamps):
    __tablename__ = 'currencies'

    id = Column(BigInteger, primary_key=True)
    ticker = Column(Text, nullable=False)

    def __init__(self, ticker):
        self.ticker = ticker


class CurrencyRate(Base, ModelWithTimestamps):
    __tablename__ = 'currency_rates'

    currency_from_id = Column(BigInteger, ForeignKey(Currency.id), nullable=False, primary_key=True)
    currency_to_id = Column(BigInteger, ForeignKey(Currency.id), nullable=False, primary_key=True)

    currency_from = relationship(Currency)
    currency_to = relationship(Currency)

    def __init__(self, currency_from_id, currency_to_id):
        self.currency_from_id = currency_from_id
        self.currency_to_id = currency_to_id


class TransferRule(Base, ModelWithTimestamps):
    __tablename__ = 'exchange_rules'

    TYPE_INTERNAL_TRANSFER = 100
    TYPE_EXTERNAL_TRANSFER = 200

    id = Column(BigInteger, primary_key=True)
    type = Column(BigInteger, nullable=False, unique=True)
    percent = Column(Numeric, nullable=False, server_default='0')
