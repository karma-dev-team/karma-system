from enum import Enum


class UserRoles(Enum):
    player = 'player'
    server_owner = 'server_owner'
    admin = 'admin'
    moderator = 'moderator'
    user = 'user'
