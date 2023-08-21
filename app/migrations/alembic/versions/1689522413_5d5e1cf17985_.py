"""

Message: empty message
Revision ID: 5d5e1cf17985
Revises: 42c64b82b166
Create Date: 2023-07-16 22:46:53.275357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d5e1cf17985'
down_revision = '42c64b82b166'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('device_token', sa.String(length=256), nullable=True),
    sa.Column('device_type', sa.Enum('ios', 'android', name='devicetype'), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('device_token')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('device')
    # ### end Alembic commands ###