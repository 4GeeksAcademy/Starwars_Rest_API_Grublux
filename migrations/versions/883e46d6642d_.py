"""empty message

Revision ID: 883e46d6642d
Revises: 3c5dd77f84dd
Create Date: 2024-03-19 16:43:49.731630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '883e46d6642d'
down_revision = '3c5dd77f84dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
