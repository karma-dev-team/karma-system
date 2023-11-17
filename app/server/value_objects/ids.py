from __future__ import annotations


from app.base.typeid import TypeID


class ServerID(TypeID):
	prefix = "server"


class PlayerID(TypeID):
	prefix = 'player'
