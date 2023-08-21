"""

Message: empty message
Revision ID: cba50694c52a
Revises: 56483f59f7bc
Create Date: 2023-05-30 22:21:50.385462

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cba50694c52a'
down_revision = '56483f59f7bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tutor_grade')
    op.add_column('tutor_subject', sa.Column('grade_id', sa.Integer(), nullable=False))
    op.add_column('tutor_subject', sa.Column('price', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tutor_subject', 'price')
    op.drop_column('tutor_subject', 'grade_id')
    op.create_table('tutor_grade',
                    sa.Column('tutor_id', mysql.INTEGER(), autoincrement=False, nullable=False),
                    sa.Column('grade_id', mysql.INTEGER(), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('tutor_id', 'grade_id'),
                    mysql_collate='utf8mb4_0900_ai_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB'
                    )
    # ### end Alembic commands ###
