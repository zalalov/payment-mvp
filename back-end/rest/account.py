from flask_restful import Resource
from flask import request, abort, jsonify, url_for, make_response, g
from decimal import Decimal

from models import User, Account, Event
from users import create_user
from decorators import login_required
from events import create_event
from exceptions import AccountHasntEnoughMoneyException


class Accounts(Resource):
    @login_required
    def get(self, *args, **kwargs):
        return {'data': [account.to_json(private=True) for account in g.current_user.accounts]}, 200


class AccountTransfer(Resource):
    @login_required
    def post(self, *args, **kwargs):
        account_from_id = request.json.get('account_from_id')
        account_to_id = request.json.get('account_to_id')
        amount = request.json.get('amount')

        account_from = Account.query.get(account_from_id)
        account_to = Account.query.get(account_to_id)

        if not account_from:
            abort(404, 'Sender account does not exists.')

        if not account_to:
            abort(404, 'Receiver account does not exists.')

        if not g.current_user.is_account_owner(account_from) and not g.current_user.is_admin():
            abort(403, 'You don\'t have permissions to make a transfer.')

        if not amount:
            abort(400, 'Invalid amount.')

        amount = Decimal(amount)
        message = 'Successful transfer'
        event = None

        try:
            event = create_event(g.current_user, account_from, account_to, amount)

            if event.status == Event.STATUS_SUCCESS:
                return {}, 200
        except AccountHasntEnoughMoneyException as e:
            return {'message': 'Account has not enough money. Probably transfer unable to take fee from your account.'}, 200

        return {'message': 'Transfer failed, we\'re working on it'}, 400
