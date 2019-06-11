"""new_relations

Revision ID: c29face11cf3
Revises: 2eb8da6c7c12
Create Date: 2019-06-11 15:55:40.262797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c29face11cf3'
down_revision = '2eb8da6c7c12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('currency_id', sa.BigInteger(), nullable=False))
    op.add_column('events', sa.Column('account_from_id', sa.BigInteger(), nullable=False))
    op.add_column('events', sa.Column('account_to_id', sa.BigInteger(), nullable=False))
    op.alter_column('events', 'type',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.create_foreign_key(None, 'events', 'accounts', ['account_from_id'], ['id'])
    op.create_foreign_key(None, 'events', 'accounts', ['account_to_id'], ['id'])
    op.drop_constraint('transactions_account_from_id_fkey', 'transactions', type_='foreignkey')
    op.drop_constraint('transactions_account_to_id_fkey', 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'account_to_id')
    op.drop_column('transactions', 'account_from_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('account_from_id', sa.BIGINT(), autoincrement=False, nullable=False))
    op.add_column('transactions', sa.Column('account_to_id', sa.BIGINT(), autoincrement=False, nullable=False))
    op.create_foreign_key('transactions_account_to_id_fkey', 'transactions', 'accounts', ['account_to_id'], ['id'])
    op.create_foreign_key('transactions_account_from_id_fkey', 'transactions', 'accounts', ['account_from_id'], ['id'])
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.drop_constraint(None, 'events', type_='foreignkey')
    op.alter_column('events', 'type',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.drop_column('events', 'account_to_id')
    op.drop_column('events', 'account_from_id')
    op.drop_column('accounts', 'currency_id')
    # ### end Alembic commands ###
