"""orderıtem

Revision ID: 6dd4088cc750
Revises: 0690347dcd11
Create Date: 2025-05-04 18:03:49.237743

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6dd4088cc750'
down_revision = '0690347dcd11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_constraint('orders_ibfk_1', type_='foreignkey')
        batch_op.drop_column('book_id')
        batch_op.drop_column('total_price')
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('total_price', mysql.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('book_id', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('orders_ibfk_1', 'books', ['book_id'], ['id'])

    # ### end Alembic commands ###
