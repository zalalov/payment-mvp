from sqlalchemy import Column, BigInteger, Numeric, DateTime, Text, func

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

    def to_json(self):
        to_serialize = [
            'id',
            'login'
        ]
        d = {}

        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)

        return d


class User(Base, ModelWithTimestamps):
    __tablename__ = 'users'

    GENDER_MALE = 10
    GENDER_FEMAIL = 20
    GENDER_OTHER = 30
    GENDER_NONE = 40

    id = Column(BigInteger, primary_key=True)
    login = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    salt = Column(Text, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def to_json(self):
        to_serialize = [
            'id',
            'login',
        ]
        d = {}

        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)

        return d


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
    user_id = Column(BigInteger, nullable=False)
    balance = Column(Numeric, nullable=False, default=0)

    def __init__(self, user_id, type, balance):
        if type not in self.AVAILABLE_TYPES:
            raise InvalidModelProperties()

        self.user_id = user_id
        self.balance = balance

    def to_json(self):
        to_serialize = [
            'id',
            'user_id',
            'balance',
        ]
        d = {}

        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)

        return d


class Transaction(Base, ModelWithTimestamps):
    __tablename__ = 'transactions'

    id = Column(BigInteger, primary_key=True)
    value = Column(Numeric, nullable=False)
    account_from_id = Column(BigInteger, nullable=False)
    account_to_id = Column(BigInteger, nullable=False)

    def __init__(self, value, account_from_id, account_to_id):
        self.value = value
        self.account_from_id = account_from_id
        self.account_to_id = account_to_id

    def to_json(self):
        to_serialize = [
            'id',
            'value',
            'account_from_id',
            'account_to_id',
        ]
        d = {}

        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)

        return d
