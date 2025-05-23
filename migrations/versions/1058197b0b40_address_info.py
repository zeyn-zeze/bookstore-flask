"""address info

Revision ID: 1058197b0b40
Revises: cb3f82d6cdde
Create Date: 2025-05-04 18:53:14.548437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1058197b0b40'
down_revision = 'cb3f82d6cdde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('address')

    # ### end Alembic commands ###
