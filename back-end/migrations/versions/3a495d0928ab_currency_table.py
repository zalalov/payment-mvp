"""currency_table

Revision ID: 3a495d0928ab
Revises: 48e7c658a8b4
Create Date: 2019-06-11 14:20:15.845953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a495d0928ab'
down_revision = '48e7c658a8b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currencies',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('ticker', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('currencies')
    # ### end Alembic commands ###