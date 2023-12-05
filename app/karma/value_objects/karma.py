from __future__ import annotations

from typing import Any

from _decimal import Decimal, InvalidOperation
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


DecimalOrNumber = Decimal | float | int


class KarmaAmount(Decimal):  # standalone value object
    __slots__ = "_value"

    # don't add __slots__, because this object becames not iterable by vars function
    # vars is used by fastapi.jsonable_encoder, this is way fastapi can encode objects
    def __init__(self, value: Amount | DecimalOrNumber):
        try:
            self._value = Decimal(str(value))
        except InvalidOperation as exc:
            raise ValueError("Invalid amount value", value) from exc

    def is_zero(self) -> bool:
        return self._value.is_zero()

    def to_decimal(self) -> Decimal:
        return self._value

    def __add__(self, other: Amount | DecimalOrNumber):
        if isinstance(other, self.__class__):
            return self.__class__(self._value + other._value)

        new_value = self._value + Decimal(str(other))
        return self.__class__(new_value)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self._value - other._value)

        new_value = self._value - Decimal(str(other))
        return self.__class__(new_value)

    def __str__(self):
        return str(self._value)

    def __mul__(self, other: Amount | DecimalOrNumber):
        if isinstance(other, self.__class__):
            return self.__class__(self._value * other._value)

        new_value = self._value * Decimal(str(other))
        return self.__class__(new_value)

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

        def validate_from_decimal(value: DecimalOrNumber) -> Amount:
            result = cls(value)
            return result

        from_decimal_schema = core_schema.chain_schema(
            [
                core_schema.decimal_schema(),
                core_schema.no_info_plain_validator_function(validate_from_decimal),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_decimal_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(cls),
                    from_decimal_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: instance
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
            cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(core_schema.decimal_schema(allow_inf_nan=False))
