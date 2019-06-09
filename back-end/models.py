from sqlalchemy import Column, BigInteger, Numeric, DateTime, Text, func

from database import Base


class ModelWithTimestamps:
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now())


class User(Base, ModelWithTimestamps):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    salt = Column(Text, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def to_json(self):
        to_serialize = [
            'id',
            'user_id',
            'balance',
            'account_to_id',
            'created_at',
            'updated_at',
        ]
        d = {}

        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)

        return d


class Account(Base, ModelWithTimestamps):
    __tablename__ = 'accounts'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    balance = Column(Numeric, nullable=False)

    def __init__(self, user_id, balance):
        self.user_id = user_id
        self.balance = balance

    def to_json(self):
        to_serialize = [
            'id',
            'user_id',
            'balance',
            'account_to_id',
            'created_at',
            'updated_at',
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
            'created_at',
            'updated_at',
        ]
        d = {}

        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)

        return d

