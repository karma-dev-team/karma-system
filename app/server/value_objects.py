from __future__ import annotations
from decimal import Decimal, InvalidOperation

from app.base.typeid import TypeID


class ServerID(TypeID):
	prefix = "server"


class IPv4Address:
	pass


DecimalOrNumber = Decimal | float | int


class Amount(Decimal):  # standalone value object
	__slots__ = "_value"

	# don't add __slots__, because this object becames not iterable by vars function
	# vars is used by fastapi.jsonable_encoder, this is way fastapi can encode objects
	def __init__(self, value: Amount | DecimalOrNumber):
		try:
			self._value = Decimal(str(value))
		except InvalidOperation as exc:
			raise ValueError("Invalid amount value", value) from exc

	def is_zero(self) -> bool:
		return self._value.is_zero()

	def to_decimal(self) -> Decimal:
		return self._value

	def __add__(self, other: Amount | DecimalOrNumber):
		if isinstance(other, self.__class__):
			return self.__class__(self._value + other._value)

		new_value = self._value + Decimal(str(other))
		return self.__class__(new_value)

	def __sub__(self, other):
		if isinstance(other, self.__class__):
			return self.__class__(self._value - other._value)

		new_value = self._value - Decimal(str(other))
		return self.__class__(new_value)

	def __str__(self):
		return str(self._value)

	def __mul__(self, other: Amount | DecimalOrNumber):
		if isinstance(other, self.__class__):
			return self.__class__(self._value * other._value)

		new_value = self._value * Decimal(str(other))
		return self.__class__(new_value)


ServerKarmaAmount = Amount
