from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.base.api.middlewares.content_size_limit import ContentSizeLimitMiddleware

origins = [
    "http://localhost",
    "http://localhost:8000",
]


def load_middlewares(
        app: FastAPI,
        debug: bool = False
) -> None:
    # app.add_middleware(DatabaseSessionMiddleware, session_factory=session_maker)
    # app.add_middleware(CSRFMiddleware, secret=secret_key)  # TODO: ДОБАВИТЬ ПОДДЕРЖКУ ПРИ ВЫПУСКЕ В ПРОДУ
    if debug:
        # дает разрешение отправлять любым хостам на бекенд свои запросы.
        # что очень не безапасно
        origins.append("*")
    app.add_middleware(
        ContentSizeLimitMiddleware, max_content_size=2048
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
