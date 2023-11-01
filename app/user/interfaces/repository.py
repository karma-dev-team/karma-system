from app.base.value_objects.ids import UIDValueObject


class AbstractUserRepo:
	async def get_user_by_id(self, user_id: UIDValueObject):
		pass
