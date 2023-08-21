"""

Message: empty message
Revision ID: e60101862ad3
Revises: 
Create Date: 2023-05-20 15:22:58.182774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e60101862ad3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grade',
    sa.Column('name', sa.String(length=256), nullable=True, comment='name of Grade like: Lớp 1'),
    sa.Column('description', sa.String(length=256), nullable=True, comment='Mô tả'),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subject',
    sa.Column('name', sa.String(length=256), nullable=True, comment='name of subject'),
    sa.Column('description', sa.String(length=256), nullable=True, comment='Mô tả'),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('full_name', sa.String(length=256), nullable=True, comment='Full Name User'),
    sa.Column('phone_number', sa.String(length=12), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('password', sa.String(length=1024), nullable=True),
    sa.Column('salt', sa.String(length=256), nullable=True, comment='Salt for hash password'),
    sa.Column('role', sa.Enum('tutor', 'parent', 'student', name='usertype'), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('otp',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('otp_code', sa.String(length=6), nullable=False),
    sa.Column('expiration_timestamp', sa.DateTime(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parent',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tutor',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('literacy', sa.Enum('college_student', 'teacher', 'lecturers', name='literacy'), nullable=True),
    sa.Column('achievement', sa.String(length=1024), nullable=True),
    sa.Column('school', sa.String(length=1024), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('grade_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['grade_id'], ['grade.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tutor_grade',
    sa.Column('tutor_id', sa.Integer(), nullable=False),
    sa.Column('grade_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['grade_id'], ['grade.id'], ),
    sa.ForeignKeyConstraint(['tutor_id'], ['tutor.user_id'], ),
    sa.PrimaryKeyConstraint('tutor_id', 'grade_id')
    )
    op.create_table('tutor_subject',
    sa.Column('tutor_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['tutor_id'], ['tutor.user_id'], ),
    sa.PrimaryKeyConstraint('tutor_id', 'subject_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tutor_subject')
    op.drop_table('tutor_grade')
    op.drop_table('tutor')
    op.drop_table('student')
    op.drop_table('parent')
    op.drop_table('otp')
    op.drop_table('user')
    op.drop_table('subject')
    op.drop_table('grade')
    # ### end Alembic commands ###