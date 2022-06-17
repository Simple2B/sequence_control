"""added milestone_id 

Revision ID: 4a2e249554e7
Revises: e4ac70f3db4f
Create Date: 2022-06-15 13:06:34.657155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a2e249554e7'
down_revision = 'e4ac70f3db4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('plan_dates', 'version',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('works', sa.Column('milestone_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('works', 'milestone_id')
    op.alter_column('plan_dates', 'version',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###