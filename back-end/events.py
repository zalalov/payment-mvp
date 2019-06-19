from models import Event, Fee
from exceptions import AccountHasntEnoughMoneyException
from transactions import transfer, convert
from app import db, app
from users import get_admin_account


def create_event(user, account_from, account_to, amount):
    fee = db.session.query(Fee).filter(Fee.type == Fee.TYPE_INTERNAL_TRANSFER).one()

    if account_from.user_id != account_to.user_id:
        fee = db.session.query(Fee).filter(Fee.type == Fee.TYPE_EXTERNAL_TRANSFER).one()

    if not account_from.has_enough_funds(amount * (1 + fee.percent)):
        raise AccountHasntEnoughMoneyException()

    event = Event()
    event.user = user

    db.session.add(event)
    db.session.commit()

    try:
        if account_from.currency != account_to.currency:
            _account_from = account_from.user.get_account_by_currency(account_to.currency)

            converted_amount = convert(db.session, event, account_from, _account_from, amount)
            convert(db.session, event, account_from, _account_from, amount * fee.percent)

            account_from = _account_from
            amount = converted_amount

        admin_account = get_admin_account()
        transfer(
            db.session,
            event,
            account_from,
            account_to,
            amount,
            admin_account.get_account_by_currency(account_from.currency)
        )

        event.status = Event.STATUS_SUCCESS
    except Exception as e:
        app.logger.error(str(e))

        event.status = Event.STATUS_FAILED

    db.session.commit()

    return event
