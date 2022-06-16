"""reason_id 

Revision ID: d8814e7a5b6e
Revises: 6c85f9b7a2e2
Create Date: 2022-06-16 13:07:44.215894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8814e7a5b6e'
down_revision = '6c85f9b7a2e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('works', sa.Column('reason_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('works', 'reason_id')
    # ### end Alembic commands ###
