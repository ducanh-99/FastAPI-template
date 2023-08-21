"""

Message: empty message
Revision ID: c119578c29f5
Revises: ac6acb75da5f
Create Date: 2023-06-04 21:52:33.562712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c119578c29f5'
down_revision = 'ac6acb75da5f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('booking_ibfk_4', 'booking', type_='foreignkey')
    op.drop_constraint('booking_ibfk_1', 'booking', type_='foreignkey')
    op.drop_constraint('booking_ibfk_2', 'booking', type_='foreignkey')
    op.create_foreign_key(None, 'booking', 'user', ['student_id'], ['id'])
    op.create_foreign_key(None, 'booking', 'user', ['parent_id'], ['id'])
    op.create_foreign_key(None, 'booking', 'user', ['tutor_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'booking', type_='foreignkey')
    op.drop_constraint(None, 'booking', type_='foreignkey')
    op.drop_constraint(None, 'booking', type_='foreignkey')
    op.create_foreign_key('booking_ibfk_2', 'booking', 'student', ['student_id'], ['id'])
    op.create_foreign_key('booking_ibfk_1', 'booking', 'parent', ['parent_id'], ['id'])
    op.create_foreign_key('booking_ibfk_4', 'booking', 'tutor', ['tutor_id'], ['user_id'])
    # ### end Alembic commands ###
