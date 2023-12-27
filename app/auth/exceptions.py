from fastapi import Request
from fastapi.responses import ORJSONResponse
from fastapi_csrf_protect.exceptions import CsrfProtectError

from app.base.exceptions import ApplicationError, exception_wrapper


@exception_wrapper
class AccessDenied(ApplicationError):
    def message(self) -> str:
        return "Access denied, no session id or not correct"


def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return ORJSONResponse(status_code=exc.status_code, content={"detail": exc.message})
