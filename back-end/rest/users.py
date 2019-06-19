from flask_restful import Resource
from flask import request, abort, jsonify, url_for, make_response, g

from models import User
from users import create_user
from decorators import login_required


class UserRegistration(Resource):
    def post(self, *args, **kwargs):
        login = request.json.get('login')
        password = request.json.get('password')
        confirmation = request.json.get('confirmation')

        if not all([login, password, confirmation]):
            return {'message': 'Login, password, confirmation fields required.'}, 400

        if password != confirmation:
            return {'message': 'Password and confirmation have to be equal.'}, 400

        if User.query.filter_by(login=login).first() is not None:
            return {'message': 'User with the same login already exists.'}, 400

        user = create_user(login, password)
        auth_token = user.encode_auth_token()

        return {'token': auth_token.decode('utf-8')}, 201


class UserLogin(Resource):
    def post(self, *args, **kwargs):
        login = request.json.get('login')
        password = request.json.get('password')

        user = User.find_by_login(login)

        if not user:
            return {'message': 'User not found.'}, 404

        if not user.validate_user_password(password):
            return {'message': 'Password is invalid.'}, 403

        auth_token = user.encode_auth_token()

        return {'message': 'Logged in as {}'.format(user.login), 'token': auth_token.decode('utf-8')}, 200


class UserLogout(Resource):
    @login_required
    def post(self, *args, **kwargs):
        if not g.current_user:
            abort(403, {'message': 'You are not logged in.'})

        g.current_user = None

        return {'message': 'Successfully loged out.'}, 200


class Users(Resource):
    @login_required
    def get(self, *args, **kwargs):
        g.current_user = None

        return {'data': [user.to_json() for user in User.query.all()]}, 200


class UserAccounts(Resource):
    @login_required
    def get(self, id, *args, **kwargs):
        user = User.query.get(id)

        if not user:
            abort(404, 'User not found.')

        return {'data': [account.to_json() for account in user.accounts]}, 200
