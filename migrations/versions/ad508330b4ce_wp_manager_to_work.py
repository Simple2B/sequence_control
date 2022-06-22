"""wp_manager to work

Revision ID: ad508330b4ce
Revises: 09402c1abe6d
Create Date: 2022-06-21 17:44:53.093299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad508330b4ce'
down_revision = '09402c1abe6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('works', sa.Column('wp_manager_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'works', 'users', ['wp_manager_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'works', type_='foreignkey')
    op.drop_column('works', 'wp_manager_id')
    # ### end Alembic commands ###