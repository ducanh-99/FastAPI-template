"""

Message: empty message
Revision ID: 7937b3f3a453
Revises: 948df51991cb
Create Date: 2023-05-23 23:22:27.435888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7937b3f3a453'
down_revision = '948df51991cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tutor_grade_ibfk_2', 'tutor_grade', type_='foreignkey')
    op.drop_constraint('tutor_grade_ibfk_1', 'tutor_grade', type_='foreignkey')
    op.drop_constraint('tutor_subject_ibfk_1', 'tutor_subject', type_='foreignkey')
    op.drop_constraint('tutor_subject_ibfk_2', 'tutor_subject', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('tutor_subject_ibfk_2', 'tutor_subject', 'tutor', ['tutor_id'], ['user_id'])
    op.create_foreign_key('tutor_subject_ibfk_1', 'tutor_subject', 'subject', ['subject_id'], ['id'])
    op.create_foreign_key('tutor_grade_ibfk_1', 'tutor_grade', 'grade', ['grade_id'], ['id'])
    op.create_foreign_key('tutor_grade_ibfk_2', 'tutor_grade', 'tutor', ['tutor_id'], ['user_id'])
    # ### end Alembic commands ###