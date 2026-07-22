import re
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Generator

from pydantic import BaseModel, ConfigDict, SerializationInfo, model_serializer
from pydantic.functional_serializers import SerializerFunctionWrapHandler

# Request-scoped normalization policy for extra fields.
#
# Default (False) is passthrough: extra fields are sent/exposed exactly as
# given by the caller/server. Setting this to True for the duration of a
# scope restores the legacy auto-conversion (camelCase on the wire,
# snake_case on Python attributes) that this SDK used before passthrough
# became the default.
#
# This is deliberately a transitional mechanism: `legacy_extra_fields_normalization`
# is expected to be removed in 3.0, once passthrough is the only behavior.
# Keeping it confined to a ContextVar plus the two hooks below.
#
# The scope is opened once per request, around `HTTPTransport.request()`,
# which is the one place that knows which client's `Configuration` a given
# call belongs to.
_legacy_extra_fields_normalization: ContextVar[bool] = ContextVar(
    "legacy_extra_fields_normalization", default=False
)


@contextmanager
def legacy_extra_fields_normalization_scope(enabled: bool) -> Generator[None, None, None]:
    """Scope the extra-field normalization policy for the duration of the block.

    :param enabled: When True, extra fields are auto-converted matching the
        legacy behavior. When False, extra fields pass
        through untouched in both directions.
    """
    token = _legacy_extra_fields_normalization.set(enabled)
    try:
        yield
    finally:
        _legacy_extra_fields_normalization.reset(token)


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
    """Normalize extra keys to ``snake_case``, at validation time and at dump time.

    Only applies when the legacy scope (:func:`legacy_extra_fields_normalization_scope`)
    is active; otherwise extra keys pass through exactly as given.

    Two hooks are needed because it is used as a base for both
    response and request models:

    - As a response base, extras are normalized in ``model_post_init``
      (construction time), so that attribute access (``response.extra_field``)
      reflects the policy.
    - As a request base, the
      model is constructed earlier, in the public API method, before that
      scope starts, so ``model_post_init`` alone would always see the
      ambient default. The ``model_serializer`` below re-checks the policy
      at dump time instead, when it's invoked from ``request_body()``
    """

    def model_post_init(self, __context: Any) -> None:
        if not _legacy_extra_fields_normalization.get():
            return
        extra = self.__pydantic_extra__
        if extra:
            self.__pydantic_extra__ = {_to_snake_case(k): v for k, v in extra.items()}

    @model_serializer(mode="wrap")
    def _serialize_with_snake_extras(
        self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> dict:
        data = handler(self)
        if not _legacy_extra_fields_normalization.get():
            return data

        extra_keys = set(getattr(self, "__pydantic_extra__", None) or {})
        if not extra_keys:
            return data
        return {
            (_to_snake_case(k) if k in extra_keys else k): v
            for k, v in data.items()
        }


class _CamelizeKeysOnDump:
    """Recursively rewrite every dict key in the serialized output to
    ``camelCase`` when ``by_alias=True``.

    Only applies when the legacy scope (:func:`legacy_extra_fields_normalization_scope`)
    is active; otherwise the serialized output passes through unchanged.
    """

    @model_serializer(mode="wrap")
    def _serialize_with_camel_extras(
        self, handler: SerializerFunctionWrapHandler, info: SerializationInfo
    ) -> dict:
        data = handler(self)
        if info.by_alias and _legacy_extra_fields_normalization.get():
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

