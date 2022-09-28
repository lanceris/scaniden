"""Alter expires_at

Revision ID: c5200a5d96c8
Revises: 72b5f009e104
Create Date: 2022-09-27 23:24:35.687881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5200a5d96c8'
down_revision = '72b5f009e104'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('identities', 'expires_at',
               existing_type=sa.DATE(),
               nullable=True)


def downgrade() -> None:
    op.alter_column('identities', 'expires_at',
               existing_type=sa.DATE(),
               nullable=False)
