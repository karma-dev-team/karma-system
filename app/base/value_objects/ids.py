from uuid import UUID

from app.base.value_object import value_object


@value_object
class UIDValueObject:
	id: UUID

	def generate(self):
		pass 


@value_object
class IPUIDValueObject:
	pass
