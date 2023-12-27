from dataclasses import dataclass
from typing import TypeVar, Generic

from fastapi import FastAPI, status, Request, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic.v1.generics import GenericModel
from starlette.responses import HTMLResponse, RedirectResponse

from app.auth.exceptions import AccessDenied
from app.base.logging.logger import get_logger


logger = get_logger(__name__)


TData = TypeVar("TData")


@dataclass(frozen=True)
class ErrorResult(GenericModel, Generic[TData]):
    message: str
    data: TData


async def handle_403_access_denied(request: Request, err: AccessDenied):
    response = RedirectResponse("/", status_code=403)
    return response


async def handle_404_not_found(request: Request, err: HTTPException):
    return RedirectResponse('/')


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResult(message="Unknown server error has occurred", data=err),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def load_basic_exceptions_handlers(app: FastAPI):
    app.add_exception_handler(AccessDenied, handle_403_access_denied)
    app.add_exception_handler(Exception, unknown_exception_handler)
    app.add_exception_handler(404, handle_404_not_found)
