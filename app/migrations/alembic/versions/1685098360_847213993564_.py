"""

Message: empty message
Revision ID: 847213993564
Revises: d0fcb10c32ef
Create Date: 2023-05-26 17:52:40.970457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '847213993564'
down_revision = 'd0fcb10c32ef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('device_code', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'device_code')
    # ### end Alembic commands ###
