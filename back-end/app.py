from sqlalchemy import MetaData
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from config import get_configuration

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

app = Flask(__name__)
app.config.from_object(get_configuration())

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
api = Api(app, prefix='/api')

from rest import users, events, account

api.add_resource(users.UserRegistration, '/register')
api.add_resource(users.UserLogin, '/login')
api.add_resource(users.UserLogout, '/logout')
api.add_resource(users.Users, '/users')

api.add_resource(events.Events, '/events')

api.add_resource(account.Accounts, '/accounts')
