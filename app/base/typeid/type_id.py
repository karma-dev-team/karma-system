import uuid
from typing import NoReturn
from uuid import UUID

from app.base.typeid.consts import PREFIX_MAX_LEN
from app.base.typeid.exceptions import PrefixValidationException, InvalidTypeIDStringException


class TypeID:
	"""
	Usage:

	class UserID(TypeID):
		prefix = "user"

	API:
	UserID.from_uuid(uuid.uuid4())
	"""

	prefix: str

	def __init__(self, *, suffix: UUID | None = None):
		self.suffix = uuid.uuid4() if not suffix else suffix

	@classmethod
	def from_uuid(cls, uuid_instance: UUID) -> "TypeID":
		return TypeID(suffix=uuid_instance)

	@classmethod
	def from_string(cls, string: str) -> "TypeID":
		prefix, suffix = get_prefix_and_suffix(string)
		if prefix != cls.prefix:
			raise PrefixValidationException(f'Wrong prefix: {prefix}, class prefix: {cls.prefix}')
		return TypeID(suffix=UUID(suffix))

	@property
	def uuid(self) -> UUID:
		return self.suffix

	def __str__(self):
		value = ""
		if self.prefix:
			value += f"{self.prefix}_"
		value += self.suffix
		return value

	def __eq__(self, value: object) -> bool:
		if not isinstance(value, self.__class__):
			return False
		return value.suffix == self.suffix

	def __hash__(self) -> int:
		return hash((self.prefix, self.suffix))


def validate_prefix(prefix: str) -> NoReturn:
	if not prefix.islower() or not prefix.isascii() or len(prefix) > PREFIX_MAX_LEN or not prefix.isalpha():
		raise PrefixValidationException(f"Invalid prefix: {prefix}.")


def get_prefix_and_suffix(string: str) -> tuple:
	parts = string.split("_")
	prefix = None
	if len(parts) == 1:
		suffix = parts[0]
	elif len(parts) == 2 and parts[0] != "":
		suffix = parts[1]
		prefix = parts[0]
	else:
		raise InvalidTypeIDStringException(f"Invalid TypeID: {string}")

	return prefix, suffix
