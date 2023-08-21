"""

Message: empty message
Revision ID: 75d8df86e0be
Revises: 6f585ba88bb4
Create Date: 2023-08-02 22:26:16.095942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75d8df86e0be'
down_revision = '6f585ba88bb4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('device_status', sa.Enum('delete', 'active', name='devicestatus'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'device_status')
    # ### end Alembic commands ###
