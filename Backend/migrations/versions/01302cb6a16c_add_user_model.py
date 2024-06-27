"""Add User model

Revision ID: 01302cb6a16c
Revises: 768b00a85433
Create Date: 2024-06-27 14:36:03.544636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01302cb6a16c'
down_revision = '768b00a85433'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###