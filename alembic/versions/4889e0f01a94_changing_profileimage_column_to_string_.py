"""Changing profileImage column to string type

Revision ID: 4889e0f01a94
Revises: c782c9880d64
Create Date: 2022-06-04 01:36:15.554395

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = '4889e0f01a94'
down_revision = 'c782c9880d64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'users',
        'profileImage',
        existing_type=postgresql.BYTEA(),
        type_=sa.String(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'users',
        'profileImage',
        existing_type=sa.String(),
        type_=postgresql.BYTEA(),
        existing_nullable=True,
    )
    # ### end Alembic commands ###
