from flask_restful import Resource
from flask import request, abort, jsonify, url_for, make_response, g

from models import User, Account
from users import create_user, login_required
from events import create_event


class Accounts(Resource):
    @login_required
    def get(self, *args, **kwargs):
        return {'data': [account.to_json() for account in g.current_user.accounts]}, 200

    @login_required
    def post(self, *args, **kwargs):
        data = request.json()

        account_from_id = data.get('account_from_id')
        account_to_id = data.get('account_to_id')
        amount = data.get('amount')

        account_from = Account.query.get(account_from_id)
        account_to = Account.query.get(account_to_id)

        if not account_from:
            abort(404, 'Sender account does not exists.')

        if not account_to:
            abort(404, 'Receiver account does not exists.')

        if not g.current_user.is_account_owner(account_from) or g.current_user.is_admin():
            abort(403, 'You don\'t have permissions to make a transfer.')

        if not amount:
            abort(401, 'Invalid amount.')

        return {'message': 'Successful transfer.'}
