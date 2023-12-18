"""Add registration code

Revision ID: 7a4c0c5f01f1
Revises: 
Create Date: 2023-12-15 10:15:32.113979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import app.base.database.types


# revision identifiers, used by Alembic.
revision: str = '7a4c0c5f01f1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
                    sa.Column('id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('name', sa.String(length=128), nullable=True),
                    sa.Column('description', sa.String(length=256), nullable=True),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_games'))
                    )
    op.create_index(op.f('ix_games_id'), 'games', ['id'], unique=False)
    op.create_table('players',
                    sa.Column('id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column('steam_id', sa.String(length=256), nullable=False),
                    sa.Column('ipv4', sa.String(length=128), nullable=False),
                    sa.Column('ipv6', sa.String(length=256), nullable=True),
                    sa.Column('hours', sa.DECIMAL(), nullable=True),
                    sa.Column('karma', sa.DECIMAL(), nullable=True),
                    sa.Column('online', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_players'))
                    )
    op.create_index(op.f('ix_players_id'), 'players', ['id'], unique=False)
    op.create_table('users',
                    sa.Column('id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('role', sa.Enum('player', 'admin', 'moderator', 'user', name='userroles'), nullable=False),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column('email', sa.String(length=320), nullable=False),
                    sa.Column('hashed_password', sa.String(length=256), nullable=False),
                    sa.Column('blocked', sa.Boolean(), nullable=True),
                    sa.Column('superuser', sa.Boolean(), nullable=True),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
                    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)
    op.create_table('categories',
                    sa.Column('id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column('game_id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.ForeignKeyConstraint(['game_id'], ['games.id'], name=op.f('fk_categories_game_id_games')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_categories'))
                    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_table('registration_codes',
                    sa.Column('id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('key', sa.String(length=128), nullable=False),
                    sa.Column('code', sa.String(length=128), nullable=False),
                    sa.Column('user_id', app.baserouter.database.types.GUID(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_registration_codes_user_id_users')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_registration_codes'))
                    )
    op.create_index(op.f('ix_registration_codes_id'), 'registration_codes', ['id'], unique=False)
    op.create_table('servers',
                    sa.Column('id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column('port', sa.Integer(), nullable=False),
                    sa.Column('ipv4', sa.String(length=128), nullable=False),
                    sa.Column('ipv6', sa.String(length=128), nullable=True),
                    sa.Column('owner_id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('karma', sa.DECIMAL(), nullable=True),
                    sa.Column('game_id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('country_code', sa.String(length=64), nullable=False),
                    sa.Column('registered', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['game_id'], ['games.id'], name=op.f('fk_servers_game_id_games')),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name=op.f('fk_servers_owner_id_users')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_servers'))
                    )
    op.create_index(op.f('ix_servers_id'), 'servers', ['id'], unique=False)
    op.create_table('karma_record',
                    sa.Column('id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('reason', sa.String(length=256), nullable=False),
                    sa.Column('delta_karma', sa.DECIMAL(), nullable=False),
                    sa.Column('player_id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('server_id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('duration', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['player_id'], ['players.id'], name=op.f('fk_karma_record_player_id_players')),
                    sa.ForeignKeyConstraint(['server_id'], ['servers.id'], name=op.f('fk_karma_record_server_id_servers')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_karma_record'))
                    )
    op.create_index(op.f('ix_karma_record_id'), 'karma_record', ['id'], unique=False)
    op.create_table('server_tags',
                    sa.Column('id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('name', sa.String(length=64), nullable=False),
                    sa.Column('server_id', app.baserouter.database.types.GUID(), nullable=False),
                    sa.ForeignKeyConstraint(['server_id'], ['servers.id'], name=op.f('fk_server_tags_server_id_servers')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_server_tags'))
                    )
    op.create_index(op.f('ix_server_tags_id'), 'server_tags', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_server_tags_id'), table_name='server_tags')
    op.drop_table('server_tags')
    op.drop_index(op.f('ix_karma_record_id'), table_name='karma_record')
    op.drop_table('karma_record')
    op.drop_index(op.f('ix_servers_id'), table_name='servers')
    op.drop_table('servers')
    op.drop_index(op.f('ix_registration_codes_id'), table_name='registration_codes')
    op.drop_table('registration_codes')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_players_id'), table_name='players')
    op.drop_table('players')
    op.drop_index(op.f('ix_games_id'), table_name='games')
    op.drop_table('games')
    # ### end Alembic commands ###