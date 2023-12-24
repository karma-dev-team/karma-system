from contextlib import asynccontextmanager
from typing import Callable, Mapping, Any

from fastapi import FastAPI


def lifespan(startup_callbacks: list[Callable], shutdown_callbacks: list[Callable], workflow_data: Mapping[str, Any]):
    @asynccontextmanager
    async def inner(app: FastAPI):
        for callback in startup_callbacks:
            await callback(app, workflow_data)
        yield
        for callback in shutdown_callbacks:
            await callback(app, workflow_data)

    return inner
