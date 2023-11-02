import abc
from typing import Generic, TypeVar


IT = TypeVar("IT")
OT = TypeVar("OT")


class UseCase(Generic[IT, OT]):
	@abc.abstractmethod
	async def __call__(self, dto: IT) -> OT:
		pass
