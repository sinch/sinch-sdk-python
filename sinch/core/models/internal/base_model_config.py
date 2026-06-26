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
    ## Differs from pydantic.alias_generators.to_camel in two ways:
    ##   - Empty components produced by "__" are kept as "_" instead of being
    ##     collapsed, so "foo__bar" becomes "foo_Bar" (pydantic returns "fooBar").
    ##   - The first component is lowercased verbatim, so "PHONE_NUMBER" becomes
    ##     "phoneNumber" (pydantic returns "PHONENumber").
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
    ## Differs from pydantic.alias_generators.to_snake in acronym handling:
    ## this implementation inserts an underscore before every uppercase letter,
    ## so "XMLDocURL" becomes "x_m_l_doc_u_r_l" (pydantic is acronym-aware and
    ## yields "xml_doc_url"). Kept for backwards compatibility with the previous
    ## per-domain implementations.
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()


def _camelize_keys(value: Any) -> Any:
    """Recursively camelize dict keys, walking into nested dicts and lists.

    Non-container values are returned unchanged.

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

    Implemented as a Pydantic v2 wrap serializer so the model integrates
    with both :meth:`~pydantic.BaseModel.model_dump` and
    :meth:`~pydantic.BaseModel.model_dump_json` without overriding either.
    Preserves the previous Numbers ``model_dump`` override byte-for-byte
    for the cases endpoints exercise (``by_alias=True``).
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
    """Permissive base: ``populate_by_name=True, extra="allow"`` and nothing else.

    Use for models that do not need automatic case normalization.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class SnakeCaseExtrasModel(_SnakifyExtrasOnInit, BaseConfigModel):
    """Permissive base + ``camelCase``→``snake_case`` normalization of
    ``__pydantic_extra__`` at validation time.

    Use for response models (and the Conversation shared base) where the
    consumer-facing attribute style stays ``snake_case`` regardless of the
    wire format.
    """


class CamelCaseDumpModel(_CamelizeKeysOnDump, BaseConfigModel):
    """Permissive base + recursive ``snake_case``→``camelCase`` rewrite of
    the serialized output when ``by_alias=True``.

    Use for ``camelCase``-API requests that need extras (and free-form
    dict values nested under known fields) emitted as ``camelCase`` on the
    wire. This is the role Numbers' request base played previously.
    """

