"""init

Revision ID: 2d56c3e02436
Revises: 
Create Date: 2023-06-04 02:35:55.536551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d56c3e02436'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_data',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('salaries_data',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('salary', sa.Integer(), nullable=True),
    sa.Column('next_increase_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users_data.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('salaries_data')
    op.drop_table('users_data')
    # ### end Alembic commands ###