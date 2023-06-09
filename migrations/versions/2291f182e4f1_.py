"""empty message

Revision ID: 2291f182e4f1
Revises: a87f98052f8b
Create Date: 2023-04-13 13:56:24.582805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2291f182e4f1'
down_revision = 'a87f98052f8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('climate', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planet')
    # ### end Alembic commands ###
