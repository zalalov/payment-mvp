"""initial

Revision ID: 030e5245f9c2
Revises: 
Create Date: 2019-06-12 16:25:09.791203

"""
# revision identifiers, used by Alembic.
revision = '030e5245f9c2'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
from sqlalchemy.sql import table, column
import sqlalchemy as sa
from sqlalchemy import String, BigInteger, Numeric

from config import get_configuration
from users import generate_password_hash
from models import Fee, Role


def initial_values():
    conn = op.get_bind()
    configuration = get_configuration()

    # === Initial Currency Data ===
    currency_tickers = ['USD', 'EUR', 'CNY']
    currencies_table = table(
        'currencies',
        column('ticker', String),
    )
    op.bulk_insert(
        currencies_table,
        [{'ticker': ticker} for ticker in currency_tickers]
    )
    # Default hardcoded values,
    # there should be third-party
    # service to fetch rates
    rates_initial = [
        ['USD', 'EUR', 0.88],
        ['USD', 'CNY', 6.91],
        ['EUR', 'USD', 1.13],
        ['EUR', 'CNY', 7.83],
        ['CNY', 'USD', 0.14],
        ['CNY', 'EUR', 0.12],
    ]
    currency_rates_table = table(
        'currency_rates',
        column('currency_from_id', BigInteger),
        column('currency_to_id', BigInteger),
        column('value', Numeric),
    )
    res = conn.execute("SELECT id, ticker FROM currencies")
    currencies_fetched = res.fetchall()
    tickers_map = {ticker: id for id, ticker in currencies_fetched}
    op.bulk_insert(
        currency_rates_table,
        [
            {
                'currency_from_id': tickers_map[pair[0]],
                'currency_to_id': tickers_map[pair[1]],
                'value': pair[2]
            } for pair in rates_initial
        ]
    )

    # === Initial User's & Roles data ===
    roles_table = table(
        'roles',
        column('name', String)
    )
    op.bulk_insert(
        roles_table,
        [
            {'name': Role.ROLE_ADMIN},
            {'name': Role.ROLE_REGULAR},
        ]
    )
    res = conn.execute("SELECT id FROM roles WHERE name = 'admin'")
    admin_role_id = res.fetchall()[0][0]
    users_table = table(
        'users',
        column('login', String),
        column('password', String),
        column('role_id', BigInteger),
    )
    op.bulk_insert(
        users_table,
        [
            {
                'login': configuration.ADMIN_LOGIN,
                'password': generate_password_hash(configuration.ADMIN_PASSWORD),
                'role_id': admin_role_id
            }
        ]
    )

    accounts_table = table(
        'accounts',
        column('user_id', BigInteger),
        column('balance', Numeric),
        column('currency_id', BigInteger)
    )
    op.bulk_insert(
        accounts_table,
        [{'user_id': admin_role_id, 'currency_id': currency_id} for ticker, currency_id in tickers_map.items()]
    )

    fees_table = table(
        'fees',
        column('type', BigInteger),
        column('percent', Numeric)
    )
    op.bulk_insert(
        fees_table,
        [
            {'type': Fee.TYPE_INTERNAL_TRANSFER, 'percent': 0},
            {'type': Fee.TYPE_EXTERNAL_TRANSFER, 'percent': configuration.DEFAULT_FEE},
        ]
    )


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currencies',
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('ticker', sa.Text(), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_currencies'))
                    )
    op.create_table('fees',
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('type', sa.BigInteger(), nullable=False),
                    sa.Column('percent', sa.Numeric(), server_default='0', nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_fees')),
                    sa.UniqueConstraint('type', name=op.f('uq_fees_type'))
                    )
    op.create_table('roles',
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('name', sa.Text(), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_roles')),
                    sa.UniqueConstraint('name', name=op.f('uq_roles_name'))
                    )
    op.create_table('currency_rates',
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('currency_from_id', sa.BigInteger(), nullable=False),
                    sa.Column('currency_to_id', sa.BigInteger(), nullable=False),
                    sa.Column('value', sa.Numeric(), nullable=False),
                    sa.ForeignKeyConstraint(['currency_from_id'], ['currencies.id'],
                                            name=op.f('fk_currency_rates_currency_from_id_currencies')),
                    sa.ForeignKeyConstraint(['currency_to_id'], ['currencies.id'],
                                            name=op.f('fk_currency_rates_currency_to_id_currencies')),
                    sa.PrimaryKeyConstraint('currency_from_id', 'currency_to_id', name=op.f('pk_currency_rates'))
                    )
    op.create_table('users',
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('login', sa.Text(), nullable=False),
                    sa.Column('password', sa.Text(), nullable=False),
                    sa.Column('role_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_users_role_id_roles')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
                    sa.UniqueConstraint('login', name=op.f('uq_users_login'))
                    )
    op.create_table('accounts',
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.Column('balance', sa.Numeric(), server_default='0', nullable=False),
                    sa.Column('currency_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'],
                                            name=op.f('fk_accounts_currency_id_currencies')),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_accounts_user_id_users')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_accounts'))
                    )
    op.create_table('events',
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.Column('status', sa.BigInteger(), server_default='100', nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_events_user_id_users')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_events'))
                    )
    op.create_table('transactions',
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('value', sa.Numeric(), nullable=False),
                    sa.Column('type', sa.BigInteger(), nullable=False),
                    sa.Column('event_id', sa.BigInteger(), nullable=False),
                    sa.Column('account_from_id', sa.BigInteger(), nullable=False),
                    sa.Column('account_to_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['account_from_id'], ['accounts.id'],
                                            name=op.f('fk_transactions_account_from_id_accounts')),
                    sa.ForeignKeyConstraint(['account_to_id'], ['accounts.id'],
                                            name=op.f('fk_transactions_account_to_id_accounts')),
                    sa.ForeignKeyConstraint(['event_id'], ['events.id'], name=op.f('fk_transactions_event_id_events')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_transactions'))
                    )

    initial_values()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('events')
    op.drop_table('accounts')
    op.drop_table('users')
    op.drop_table('currency_rates')
    op.drop_table('roles')
    op.drop_table('fees')
    op.drop_table('currencies')
    # ### end Alembic commands ###