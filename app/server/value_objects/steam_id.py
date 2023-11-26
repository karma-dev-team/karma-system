
from typing import Any


class SteamCommunity64(str):
	pass


class SteamCommunity32(str):
	pass


class SteamID(str):
	def __init__(self, value: Any):
		self._validate(value)

		super().__init__(value)

	def _validate(self, val: str) -> None:
		if val == "steam_0:0:0":
			raise ValueError("Steam id is local one")
		if val in ["NULL"]:
			return
		_, ids = val.split("_")

		universe, Y, acc_number = ids.split(":")
		if Y not in ["0", "1"]:
			raise ValueError("Incorrect Y: ", Y)
		if int(universe) > 12:
			raise ValueError("Incorrect Universe: ", universe)

	def to_64_steam_community(self) -> SteamCommunity64:
		# TODO
		pass

	def to_32_steam_community(self) -> SteamCommunity32:
		# TODO
		pass
