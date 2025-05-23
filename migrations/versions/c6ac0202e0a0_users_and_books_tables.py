"""Users and books tables

Revision ID: c6ac0202e0a0
Revises: 
Create Date: 2025-04-27 16:34:07.513829

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c6ac0202e0a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_data', sa.Text(), nullable=True))
        batch_op.drop_column('image_filename')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_filename', mysql.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('image_data')

    # ### end Alembic commands ###
