from exceptions import PermissionDeniedException, DBRecordNotFound, TransferDifferentCurrenciesException
from models import Transaction, CurrencyRate, Fee
from config import get_configuration


def transfer(session, event, account_from, account_to, amount, fee_account):
    configuration = get_configuration()

    if account_from == account_to:
        return

    if account_from.currency != account_to.currency:
        raise TransferDifferentCurrenciesException()

    transfer_transaction = Transaction()
    transfer_transaction.value = amount
    transfer_transaction.type = Transaction.TYPE_TRANSFER
    transfer_transaction.event = event
    transfer_transaction.account_from = account_from
    transfer_transaction.account_to = account_to

    session.add(transfer_transaction)

    account_from.balance -= amount
    account_to.balance += amount

    fee_type = Fee.TYPE_INTERNAL_TRANSFER

    if account_from.user != account_to.user:
        fee_type = Fee.TYPE_EXTERNAL_TRANSFER

    fee_percent = configuration.DEFAULT_FEE
    fee = session.query(Fee).filter(Fee.type == fee_type).one()

    if fee:
        fee_percent = fee.percent

    if fee_percent > 0:
        fee_amount = amount * fee.percent

        fee_transaction = Transaction()
        fee_transaction.value = fee_amount
        fee_transaction.type = Transaction.TYPE_FEE
        fee_transaction.event = event
        fee_transaction.account_from = account_from
        fee_transaction.account_to = fee_account

        session.add(fee_transaction)

        account_from.balance -= fee_amount
        fee_account.balance += fee_amount


def convert(session, event, account_from, account_to, amount):
    if account_from.currency == account_to.currency:
        return

    if account_from.user != account_to.user:
        raise PermissionDeniedException('Cannot convert currency externally.')

    rate = session.query(CurrencyRate).filter(
        CurrencyRate.currency_from_id == account_from.currency.id,
        CurrencyRate.currency_to_id == account_to.currency.id
    ).first()

    if not rate:
        raise DBRecordNotFound('There\'s no currency convert rate needed for the operation.')

    converted_amount = amount * rate.value

    print(amount)
    print(rate.value)
    print(converted_amount)

    transaction = Transaction()
    transaction.value = converted_amount
    transaction.type = Transaction.TYPE_CONVERT
    transaction.event = event
    transaction.account_from = account_from
    transaction.account_to = account_to

    account_from.balance -= amount
    account_to.balance += converted_amount

    session.add(transaction)

    return converted_amount
