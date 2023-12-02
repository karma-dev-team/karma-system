from enum import Enum

# костыль потому как передовать через value в маппинги алихимии
# мне лень)))
USER_ROLES_AS_INTEGER = {
    'player': 0,
    'user': 10,
    'admin': 20,
    'moderator': 30,
}


class UserRoles(Enum):
    player = 'player'
    admin = 'admin'
    moderator = 'moderator'
    user = 'user'
