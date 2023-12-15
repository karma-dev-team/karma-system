from app.base.entity import entity


@entity
class UserSession:
	session_id: str
	id: str
