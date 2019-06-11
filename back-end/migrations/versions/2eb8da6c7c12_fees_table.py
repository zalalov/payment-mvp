"""fees_table

Revision ID: 2eb8da6c7c12
Revises: 5bedd8c19691
Create Date: 2019-06-11 15:53:36.280475

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2eb8da6c7c12'
down_revision = '5bedd8c19691'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fees',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('type', sa.BigInteger(), nullable=False),
    sa.Column('percent', sa.Numeric(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type')
    )
    op.drop_table('exchange_rules')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exchange_rules',
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('type', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('percent', sa.NUMERIC(), server_default=sa.text("'0'::numeric"), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='exchange_rules_pkey'),
    sa.UniqueConstraint('type', name='exchange_rules_type_key')
    )
    op.drop_table('fees')
    # ### end Alembic commands ###
