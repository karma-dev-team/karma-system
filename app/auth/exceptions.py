from app.base.exceptions import ApplicationError, exception_wrapper


@exception_wrapper
class AccessDenied(ApplicationError):
    def message(self) -> str:
        return "Access denied, no session id or not correct"
