from app import app, db
from models import User, Currency
from config import get_configuration

if __name__ == '__main__':
    # from events import create_event
    # from users import create_user
    #
    # create_user('ruslan', '123')
    #
    # ruslan = db.session.query(User).get(2)
    # admin = db.session.query(User).get(1)
    #
    # usd = db.session.query(Currency).filter(Currency.ticker=='USD').one()
    # eur = db.session.query(Currency).filter(Currency.ticker=='EUR').one()
    # cny = db.session.query(Currency).filter(Currency.ticker=='CNY').one()
    #
    # # create_event(ruslan, ruslan.get_account_by_currency(usd), admin.get_account_by_currency(usd), 10)
    # create_event(ruslan, ruslan.get_account_by_currency(usd), admin.get_account_by_currency(eur), 10)

    configuration = get_configuration()

    app.run(host=configuration.APP_HOST, port=configuration.APP_PORT)
