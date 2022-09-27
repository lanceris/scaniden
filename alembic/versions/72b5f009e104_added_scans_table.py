"""Added scans table

Revision ID: 72b5f009e104
Revises: e5927e76d8c5
Create Date: 2022-09-27 11:09:01.860831

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '72b5f009e104'
down_revision = 'e5927e76d8c5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('scans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identity_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('verdict_value', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('scans')
