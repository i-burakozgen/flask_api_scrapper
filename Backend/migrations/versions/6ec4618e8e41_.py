"""empty message

Revision ID: 6ec4618e8e41
Revises: 
Create Date: 2024-06-25 18:24:16.680268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ec4618e8e41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pharmacy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('adress', sa.String(), nullable=False),
    sa.Column('number', sa.String(length=20), nullable=False),
    sa.Column('scrapped_at', sa.DateTime(), nullable=False),
    sa.Column('province', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pharmacy')
    # ### end Alembic commands ###
