"""add note to work

Revision ID: 95b60a85121c
Revises: d8814e7a5b6e
Create Date: 2022-06-16 16:18:44.086677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95b60a85121c'
down_revision = 'd8814e7a5b6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('works', sa.Column('note', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('works', 'note')
    # ### end Alembic commands ###
