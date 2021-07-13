"""empty message

Revision ID: 1122c30fdafb
Revises: 
Create Date: 2021-07-13 13:31:19.643638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1122c30fdafb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_address', sa.String(length=255), nullable=False),
    sa.Column('employee_name', sa.String(length=64), nullable=False),
    sa.Column('designation', sa.String(length=64), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email')
    # ### end Alembic commands ###