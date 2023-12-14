"""Add registered column

Revision ID: ce7167bfce77
Revises: 8e78c3498f65
Create Date: 2023-12-07 15:49:19.900121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce7167bfce77'
down_revision: Union[str, None] = '8e78c3498f65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('servers', sa.Column('registered', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('servers', 'registered')
    # ### end Alembic commands ###