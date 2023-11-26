from typing import Any

from pydantic import GetJsonSchemaHandler, GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class SteamCommunity64(str):
    pass


class SteamCommunity32(str):
    pass


class SteamID(str):
    def __init__(self, value: Any):
        self._validate(value)

        super().__init__(value)

    def _validate(self, val: str) -> None:
        if val == "steam_0:0:0":
            raise ValueError("Steam id is local one")
        if val in ["NULL"]:
            return
        _, ids = val.split("_")

        universe, Y, acc_number = ids.split(":")
        if Y not in ["0", "1"]:
            raise ValueError("Incorrect Y: ", Y)
        if int(universe) > 12:
            raise ValueError("Incorrect Universe: ", universe)

    @property
    def universe(self) -> str:
        return self.split(":")[0]

    def to_64_steam_community(self) -> SteamCommunity64:
        # TODO
        pass

    def to_32_steam_community(self) -> SteamCommunity32:
        # TODO
        pass

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

        def validate_from_str(value: str) -> SteamID:
            result = SteamID(value)
            return result

        from_uuid_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_uuid_schema,
            python_schema=core_schema.union_schema(
                [
                    # check if it's an instance first before doing any further work
                    core_schema.is_instance_schema(SteamID),
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
        return handler(core_schema.str_schema(max_length=20))  # should be 17
