from app.base.events.event import Event, event
from app.games.dto.category import CategoryDTO


@event
class CategoryCreated(Event):
	category: CategoryDTO
