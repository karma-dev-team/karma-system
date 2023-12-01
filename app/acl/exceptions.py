from app.base.exceptions import ApplicationError
from app.user.value_objects import UserID


class NotEnoughPermissions(ApplicationError):
	user_id: UserID

	def message(self) -> str:
		return f"Not enough permissions, id: {self.user_id}"