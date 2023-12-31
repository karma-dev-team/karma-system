"""Add description to server

Revision ID: 04191dfe480a
Revises: 4e1d3c32f2ee
Create Date: 2023-12-28 00:22:39.513551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04191dfe480a'
down_revision: Union[str, None] = '4e1d3c32f2ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('servers', sa.Column('description', sa.String(length=4096)))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('servers', 'description')
    # ### end Alembic commands ###
