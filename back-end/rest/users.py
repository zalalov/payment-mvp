from flask_restful import Resource
from flask import request, abort, jsonify, url_for, make_response, g

from models import User
from users import create_user
from users import login_required


class UserRegistration(Resource):
    def post(self, *args, **kwargs):
        login = request.json.get('login')
        password = request.json.get('password')
        confirmation = request.json.get('confirmation')

        if not all([login, password, confirmation]):
            abort(400, {'message': 'Login, password, confirmation fields required.'})

        if password != confirmation:
            abort(400, {'message': 'Password and confirmation have to be equal.'})

        if User.query.filter_by(login=login).first() is not None:
            abort(400, {'message': 'User with the same login already exists.'})

        user = create_user(login, password)
        auth_token = user.encode_auth_token()

        return {'token': auth_token.decode('utf-8')}, 201


class UserLogin(Resource):
    def post(self, *args, **kwargs):
        login = request.json.get('login')
        password = request.json.get('password')

        user = User.find_by_login(login)

        if not user:
            abort(404, {'message': 'User not found.'})

        if not user.validate_user_password(password):
            abort(403, {'message': 'Password is invalid.'})

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
