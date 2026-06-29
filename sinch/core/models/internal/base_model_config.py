import re
from typing import Any

from pydantic import BaseModel, ConfigDict, SerializationInfo, model_serializer
from pydantic.functional_serializers import SerializerFunctionWrapHandler


def _to_camel_case(snake_str: str) -> str:
    """Convert ``snake_case`` to ``camelCase`` preserving consecutive underscores.

    :param snake_str: The snake_case input string.
    :returns: The camelCase form, or the input unchanged when it contains no
        underscore.
    """
    if not snake_str or "_" not in snake_str:
        return snake_str
    components = snake_str.split("_")
    return components[0].lower() + "".join(
        (x.capitalize() if x else "_") for x in components[1:]
    )


def _to_snake_case(camel_str: str) -> str:
    """Convert ``camelCase`` to ``snake_case``.

    :param camel_str: The camelCase input string.
    :returns: The snake_case form.
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()


def _camelize_keys(value: Any) -> Any:
    """Recursively camelize dict keys, walking into nested dicts and lists.

    :param value: An arbitrary JSON-like value.
    :returns: The same structure with every ``snake_case`` dict key converted
        to ``camelCase``.
    """
    if isinstance(value, dict):
        return {_to_camel_case(k): _camelize_keys(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_camelize_keys(item) for item in value]
    return value


class _SnakifyExtrasOnInit:
    """Normalize ``__pydantic_extra__`` keys to ``snake_case`` at validation time."""

    def model_post_init(self, __context: Any) -> None:
        extra = self.__pydantic_extra__
        if extra:
            self.__pydantic_extra__ = {_to_snake_case(k): v for k, v in extra.items()}


class _CamelizeKeysOnDump:
    """Recursively rewrite every dict key in the serialized output to
    ``camelCase`` when ``by_alias=True``.
    """

    @model_serializer(mode="wrap")
    def _serialize_with_camel_extras(
        self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> dict:
        data = handler(self)
        if info.by_alias:
            data = _camelize_keys(data)
        return data


class BaseConfigModel(BaseModel):
    """Base model that allows any extra attributes.

    Use for models that do not need automatic case normalization.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class SnakeCaseExtrasModel(_SnakifyExtrasOnInit, BaseConfigModel):
    """Base model that normalizes extra attributes to ``snake_case`` at validation time.

    Use for response models where extra attributes received from the API
    should be normalized to ``snake_case`` regardless of the format returned
    by the server.
    """


class CamelCaseDumpModel(_CamelizeKeysOnDump, BaseConfigModel):
    """Base model that recursively rewrites ``snake_case`` keys to ``camelCase`` in
    the serialized output when ``by_alias=True``.

    Use for request models targeting ``camelCase`` APIs, so that extra
    attributes are emitted as ``camelCase`` in the outgoing request payload.
    """

