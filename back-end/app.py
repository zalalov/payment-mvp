import os
from sqlalchemy import MetaData
from flask import Flask, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

from config import get_configuration

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

app = Flask(__name__, static_url_path='/dist')
app.config.from_object(get_configuration())

CORS(app)

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
api = Api(app, prefix='/api')

from rest import users, events, account

api.add_resource(users.UserRegistration, '/register')
api.add_resource(users.UserLogin, '/login')
api.add_resource(users.UserLogout, '/logout')
api.add_resource(users.Users, '/users')
api.add_resource(users.UserAccounts, '/users/<int:id>/accounts')

api.add_resource(events.Events, '/events')

api.add_resource(account.Accounts, '/accounts')
api.add_resource(account.AccountTransfer, '/accounts/transfer')


# @app.route('/<path:path>')
# def send_static(path):
#     print(path)
#
#     return send_from_directory('/dist', path)
#
# @app.route('/')
# def index():
#     return send_from_directory('/dist', 'index.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    path_dir = os.path.abspath("/dist")  # path react build

    if path != "" and os.path.exists(os.path.join(path_dir, path)):
        return send_from_directory(os.path.join(path_dir), path)
    else:
        return send_from_directory(os.path.join(path_dir), 'index.html')
