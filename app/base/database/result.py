import functools
import inspect
from dataclasses import dataclass
from typing import Any, Callable, Generic, Type, TypeVar

RST = TypeVar("RST")
ET = TypeVar("ET", bound=Exception)


# custom dataclass
@dataclass(frozen=True, slots=True, match_args=True)
class Result(Generic[RST, ET]):
    value: RST | None
    exception: ET | None

    def __post_init__(self):
        if self.value is None and self.exception is None:
            raise ValueError("Result or Exception required ")
        if self.value is not None and self.exception is not None:
            raise ValueError("Result or Exception only")

    @classmethod
    def ok(cls, value: RST) -> "Result[RST, Any]":
        return cls(value=value, exception=None)

    @classmethod
    def fail(cls, exception: ET) -> "Result[Any, ET]":
        return cls(value=None, exception=exception)

    def __repr__(self):
        if self.value:
            value = self.value
            return f"<Result.ok {value=}>"
        else:
            exc = self.exception
            return f"<Result.exception {exc=}>"

    def __str__(self):
        return f"<Result value={self.value}, exception={self.exception}>"


def as_async_result(
    *exceptions: Type[ET],
) -> Callable:
    if not exceptions or not all(
            inspect.isclass(exception) and issubclass(exception, BaseException)
            for exception in exceptions
    ):
        raise TypeError("as_result() requires one or more exception types")

    def decorator(
        func: Callable,
    ):
        """
        Decorator to turn a function into one that returns a ``Result``.
        """

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Result[RST, ET]:
            try:
                return Result.ok(await func(*args, **kwargs))
            except exceptions as exc:
                return Result.fail(exc)

        return async_wrapper

    return decorator


def as_result(
    *exceptions: Type[ET],
) -> Callable:

    if not exceptions or not all(
        inspect.isclass(exception) and issubclass(exception, BaseException)
        for exception in exceptions
    ):
        raise TypeError("as_result() requires one or more exception types")

    def decorator(func: Callable) -> Callable:
        """
        Decorator to turn a function into one that returns a ``Result``.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Result[RST, ET]:
            try:
                return Result.ok(func(*args, **kwargs))
            except exceptions as exc:
                return Result.fail(exc)

        return wrapper

    return decorator
