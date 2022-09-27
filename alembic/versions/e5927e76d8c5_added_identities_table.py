"""Added identities table

Revision ID: e5927e76d8c5
Revises: 
Create Date: 2022-09-27 11:04:26.180257

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e5927e76d8c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('identities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('license_number', sa.String(length=30), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=200), nullable=True),
    sa.Column('expires_at', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('identities')
