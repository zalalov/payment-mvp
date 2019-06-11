"""events_table

Revision ID: 5bedd8c19691
Revises: d16eb59966c8
Create Date: 2019-06-11 14:51:48.101123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bedd8c19691'
down_revision = 'd16eb59966c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('type', sa.BigInteger(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('transactions', sa.Column('event_id', sa.BigInteger(), nullable=False))
    op.create_foreign_key(None, 'transactions', 'events', ['event_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'event_id')
    op.drop_table('events')
    # ### end Alembic commands ###
