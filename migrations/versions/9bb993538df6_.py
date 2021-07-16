"""empty message

Revision ID: 9bb993538df6
Revises: 90d468f5ee33
Create Date: 2021-07-16 17:58:08.105952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bb993538df6'
down_revision = '90d468f5ee33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'email', ['email_address'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'email', type_='unique')
    # ### end Alembic commands ###