"""increase varchar size

Revision ID: c2ac3a6eb22e
Revises: c5200a5d96c8
Create Date: 2022-09-27 23:29:05.393749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2ac3a6eb22e'
down_revision = 'c5200a5d96c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('identities', 'license_number',
               existing_type=sa.String(length=30),
               type_=sa.String(length=100))
    op.alter_column('identities', 'full_name',
               existing_type=sa.String(length=100),
               type_=sa.String(length=200))


def downgrade() -> None:
    op.alter_column('identities', 'license_number',
               existing_type=sa.String(length=100),
               type_=sa.String(length=30))
    op.alter_column('identities', 'full_name',
               existing_type=sa.String(length=200),
               type_=sa.String(length=100))
