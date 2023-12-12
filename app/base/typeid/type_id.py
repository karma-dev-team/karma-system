import uuid
from typing import NoReturn, Any
from uuid import UUID

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from app.base.typeid.consts import PREFIX_MAX_LEN
from app.base.typeid.exceptions import PrefixValidationException, InvalidTypeIDStringException


class TypeID:
    """
    Usage:

    class UserID(TypeID):
        prefix = "user"

    API:
    UserID.from_uuid(uuid.uuid4())
    """

    prefix: str = ""  # prefix must be singular

    def __init__(self, *, suffix: UUID | None = None, **kwargs):
        self.suffix = uuid.uuid4() if not suffix else suffix

        super().__init__(**kwargs)

    @classmethod
    def generate(cls, type_: str = "uuid4") -> "TypeID":
        if type_ == "uuid4":
            return cls(suffix=uuid.uuid4())
        elif type_ == "uuid7":
            # install uuid6
            # return cls(suffix=uuid6.uuid7())
            pass
        else:
            raise ValueError("Not supported uuid")

    @classmethod
    def from_uuid(cls, uuid_instance: UUID) -> "TypeID":
        return TypeID(suffix=uuid_instance)

    @classmethod
    def from_string(cls, string: str) -> "TypeID":
        prefix, suffix = get_prefix_and_suffix(string)
        if prefix != cls.prefix:
            raise PrefixValidationException(f'Wrong prefix: {prefix}, class prefix: {cls.prefix}')
        return TypeID(suffix=UUID(suffix))

    @property
    def uuid(self) -> UUID:
        return self.suffix

    def __str__(self):
        return str(self.suffix)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return value.suffix == self.suffix

    def __hash__(self) -> int:
        return hash((self.prefix, self.suffix))

    def __repr__(self):
        value = ""
        if self.prefix:
            value += f"{self.prefix}_"
        value += str(self.suffix)
        return value

    @classmethod
    def __get_pydantic_core_schema__(
            cls,
            _source_type: Any,
            _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """
        We return a pydantic_core.CoreSchema that behaves in the following ways:

        * ints will be parsed as `ThirdPartyType` instances with the int as the x attribute
        * `ThirdPartyType` instances will be parsed as `ThirdPartyType` instances without any changes
        * Nothing else will pass validation
        * Serialization will always return just an int
        """

        def validate_from_uuid(suffix: str | None) -> TypeID:
            result = cls(suffix=suffix)
            return result

        from_uuid_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_uuid),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_uuid_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(cls),
                    from_uuid_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(core_schema.uuid_schema(version=4))


def validate_prefix(prefix: str) -> NoReturn:
    if not prefix.islower() or not prefix.isascii() or len(prefix) > PREFIX_MAX_LEN or not prefix.isalpha():
        raise PrefixValidationException(f"Invalid prefix: {prefix}.")


def get_prefix_and_suffix(string: str) -> tuple:
    parts = string.split("_")
    prefix = None
    if len(parts) == 1:
        suffix = parts[0]
    elif len(parts) == 2 and parts[0] != "":
        suffix = parts[1]
        prefix = parts[0]
    else:
        raise InvalidTypeIDStringException(f"Invalid TypeID: {string}")

    return prefix, suffix
