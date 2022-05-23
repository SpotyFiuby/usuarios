"""test4

Revision ID: 8165ffabf0f2
Revises: fbe570c5def2
Create Date: 2022-05-23 20:13:37.700128

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '8165ffabf0f2'
down_revision = 'fbe570c5def2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'isArtist')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'users',
        sa.Column(
            'isArtist',
            sa.BOOLEAN(),
            server_default=sa.text('false'),
            autoincrement=False,
            nullable=False,
        ),
    )
    # ### end Alembic commands ###
