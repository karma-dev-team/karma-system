<<<<<<< HEAD:app/infrastructure/events/base.py
from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, Union

from .event import Event
from .middleware import BaseMiddleware

# лооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооол
# просто спиздил с https://github.com/darksidecat/cost_confirmation_bot
# лооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооол


NextMiddlewareType = Callable[[Event, Dict[str, Any]], Awaitable[Any]]
MiddlewareType = Union[
    BaseMiddleware,
    Callable[[NextMiddlewareType, Event, Dict[str, Any]], Awaitable[Any]],
]
=======
from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, Union

from .event import Event
from .middleware import BaseMiddleware

# лооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооол
# просто спиздил с https://github.com/darksidecat/cost_confirmation_bot
# лооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооол


NextMiddlewareType = Callable[[Event, Dict[str, Any]], Awaitable[Any]]
MiddlewareType = Union[
    BaseMiddleware,
    Callable[[NextMiddlewareType, Event, Dict[str, Any]], Awaitable[Any]],
]
>>>>>>> 57d1c39 (Rename infatructure to base):app/base/events/base.py
