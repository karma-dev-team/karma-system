from typing import Generic, TypeVar, Any

from attr import define

value_object = define(kw_only=True, hash=False)


VT = TypeVar("VT")


@value_object
class ValueObject(Generic[VT]):
    """
    Used only for single valued Value objects
    """
    value: VT

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return int(self.value)

    @classmethod
    def validate(cls, v: VT) -> "ValueObject":
        return cls(v)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]):
        pass

    def __attrs_post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """This method checks that a value is valid to create this value object"""
        pass


