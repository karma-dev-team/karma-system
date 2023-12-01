from typing import Any

from app.base.event import event_wrapper
from app.base.events.event import Event
from app.base.logging.logger import get_logger
from app.karma.dtos.karma import KarmaRecordDTO


logger = get_logger(__name__)


@event_wrapper
class KarmaChanged(Event):
    karma_record: KarmaRecordDTO


async def handle_karma_change(event: KarmaChanged, workflow_data: dict[str, Any]) -> None:
    # Мне лень тут передовать IoContainer
    logger.info("Karma change", extra={"event": event})
