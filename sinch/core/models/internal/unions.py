"""Deterministic resolution of the unions.

Pydantic picks a union member by its own heuristics (smart mode), which makes
the result depend on details such as optional fields or member order. Every
model union in the SDK is annotated with :class:`ResolveUnion` instead, so the
SDK decides the member before pydantic validates it.

``ResolveUnion``
    Metadata placed in ``Annotated``. It runs :func:`_resolve` on the raw
    ``dict`` before pydantic validates the union, and stores its options in a
    :class:`_UnionSpec`.

``_UnionSpec``
    - ``discriminator_strict``: ``True`` means the tag alone decides.
      ``False`` is for unions whose members have a discriminator that the
      union never declared, so pydantic resolved them in smart mode. Making
      them strict now would be a breaking change, so they fall back to
      scoring when the tag does not resolve.
    - ``tags``: tag -> member(s), read from each member's discriminator field
      unless given explicitly. A tag can map to several members, tried in
      order.
    - ``fallback``: union member taking the payloads no other member accepts.
      It exists because some unions already declare a catch-all model of
      their own, to be replaced by ``SinchRawResponse``.
    - ``shared`` / ``distinctive``: fields every member declares, and the
      rest. Only the distinctive ones count when scoring.

``parses_response`` / ``response_parsing_scope``
    The same union is used to build requests and to parse responses, and both
    need a different policy for a payload that matches no member. A
    ``ContextVar`` carries the direction:

    - Request (default): the payload is rejected with a validation error.
    - Response: the payload becomes a ``SinchRawResponse``, so a member
      the API adds later does not break an SDK that does not know it yet. A
      warning is logged each time it happens.

    ``parses_response`` decorates the entry points that parse what the API
    sends (responses and events) to switch on the response policy.

``_resolve``
    1. With a ``discriminator``, the tag (the discriminator value) is read
       from the payload and the members mapped to it are validated in order.
       The first one accepting the payload wins.
    2. If no member took the payload and ``discriminator_strict`` is ``True``,
       the resolution stops here. A request raises, unless the ``fallback``
       member accepts the payload. A response never raises: the payload goes
       to the ``fallback`` member, or to ``SinchRawResponse``.
    3. Otherwise (no discriminator, or ``discriminator_strict=False``) the
       members are ranked by scoring: one point per populated field that not
       every member declares. Members scoring zero are dropped, unless all
       do, and ties keep the declaration order. The first one accepting the
       payload wins.
    4. If nothing matched: the ``fallback`` member, then
       ``SinchRawResponse`` in responses. In requests the value is
       returned untouched and pydantic raises its usual union error.

Planned for v3 of the SDK
    The scoring goes away. Unions without a discriminator are meant to resolve
    like the discriminated ones, using as tag the field that is unique to each
    member. ``discriminator_strict=False`` and the custom ``fallback`` members
    are meant to be removed, leaving ``SinchRawResponse`` as the only
    fallback.
"""

import logging
from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    Generator,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel, GetCoreSchemaHandler, ValidationError
from pydantic.fields import FieldInfo
from pydantic_core import PydanticKnownError, core_schema

from sinch.core.models.sinch_raw_response import SinchRawResponse

__all__ = [
    "ResolveUnion",
    "response_parsing_scope",
    "parses_response",
]

logger = logging.getLogger(__name__)

#: Direction the value being validated is travelling in.
_response_parsing: ContextVar[bool] = ContextVar(
    "sinch_response_parsing", default=False
)

#: Discriminator value -> the member it selects, or the members to try in order
#: when a single value covers several shapes.
TagMap = Dict[
    str, Union[Type[BaseModel], Tuple[Type[BaseModel], ...]]
]


@contextmanager
def response_parsing_scope() -> Generator[None, None, None]:
    """Marks the block as parsing a response body.

    Union members that match nothing resolve to the union's fallback inside
    the block, and raise outside it.
    """
    token = _response_parsing.set(True)
    try:
        yield
    finally:
        _response_parsing.reset(token)


def parses_response(func: Callable) -> Callable:
    """Runs the decorated callable inside :func:`response_parsing_scope`.

    Used on the public entry points that turn a payload received from the API
    into models, so the unions they build resolve with the response policy.

    :param func: The callable parsing a response or event payload.
    :returns: The wrapped callable.
    :rtype: Callable
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with response_parsing_scope():
            return func(*args, **kwargs)

    return wrapper


def _field_keys(name: str, field: FieldInfo) -> Tuple[str, ...]:
    """Returns the payload keys that populate a field.

    :param name: The field name.
    :param field: The field definition.
    :returns: The keys, without duplicates.
    :rtype: tuple[str, ...]
    """
    keys: List[str] = []
    for key in (field.validation_alias, name):
        if isinstance(key, str) and key not in keys:
            keys.append(key)
    return tuple(keys)


def _declared_tag(model: Type[BaseModel], discriminator: str) -> Optional[str]:
    """Returns the tag a member declares, from a single-value ``Literal`` or a
    string default.

    :param model: The union member.
    :param discriminator: Name of the discriminator field.
    :returns: The declared value, or ``None`` when the member pins none.
    :rtype: Optional[str]
    """
    field = model.model_fields.get(discriminator)
    if field is None:
        return None
    if get_origin(field.annotation) is Literal:
        args = get_args(field.annotation)
        if len(args) == 1 and isinstance(args[0], str):
            return args[0]
        return None
    if isinstance(field.default, str):
        return field.default
    return None


class _UnionSpec:
    """Everything the resolver needs about one union.

    :ivar members: The union members, in declaration order.
    :ivar discriminator: Name of the discriminator field, if any.
    :ivar discriminator_strict: Whether the tag alone decides (no scoring).
    :ivar fallback: Member absorbing payloads no other member takes.
    :ivar tags: Tag -> members it selects, tried in order.
    :ivar keys: Payload keys the tag is read from (aliases and name).
    :ivar shared: Fields every member declares, ignored when scoring.
    :ivar distinctive: Member -> keys of its non-shared fields, used for
        scoring.
    """

    def __init__(
        self,
        members: Tuple[Type[BaseModel], ...],
        discriminator: Optional[str],
        discriminator_strict: bool,
        fallback: Optional[Type[BaseModel]],
        tags: Optional[TagMap],
    ) -> None:
        self.members = members
        self.discriminator = discriminator
        self.discriminator_strict = discriminator_strict
        self.fallback = fallback
        self.tags: Dict[str, Tuple[Type[BaseModel], ...]] = {}
        self.keys: Tuple[str, ...] = ()
        self.shared: FrozenSet[str] = frozenset(
            set.intersection(*[set(m.model_fields) for m in members])
            if members
            else set()
        )
        self.distinctive: Dict[Type[BaseModel], Tuple[Tuple[str, ...], ...]] = {
            member: tuple(
                _field_keys(name, field)
                for name, field in member.model_fields.items()
                if name not in self.shared
            )
            for member in members
        }
        if discriminator is None:
            return
        if tags is not None:
            self.tags = {
                tag: candidates
                if isinstance(candidates, tuple)
                else (candidates,)
                for tag, candidates in tags.items()
            }
        else:
            for member in members:
                tag = _declared_tag(member, discriminator)
                if tag is not None and tag not in self.tags:
                    self.tags[tag] = (member,)
        keys: List[str] = []
        for member in members:
            field = member.model_fields.get(discriminator)
            for key in _field_keys(discriminator, field) if field else ():
                if key not in keys:
                    keys.append(key)
        if discriminator not in keys:
            keys.append(discriminator)
        self.keys = tuple(keys)


def _read_tag(payload: Dict[str, Any], spec: _UnionSpec) -> Any:
    """Reads the discriminator value out of a raw payload.

    :param payload: The raw payload.
    :param spec: The union being resolved.
    :returns: The discriminator value, or ``None`` when absent.
    """
    for key in spec.keys:
        if key in payload:
            return payload[key]
    return None


def _score(
    payload: Dict[str, Any], model: Type[BaseModel], spec: _UnionSpec
) -> int:
    """Counts the payload keys pointing at this member rather than its siblings.

    Fields every member of the union declares carry no signal, so they are left
    out: what identifies a member is what only it declares. A key holding
    ``None`` carries none either, as callers forward unset optionals that way.

    :param payload: The raw payload.
    :param model: The union member.
    :param spec: The union being resolved.
    :returns: The number of matching distinctive fields.
    :rtype: int
    """
    return sum(
        1
        for keys in spec.distinctive[model]
        if any(payload.get(key) is not None for key in keys)
    )


def _ranked(
    payload: Dict[str, Any], spec: _UnionSpec
) -> List[Type[BaseModel]]:
    """Orders the members by how well the payload populates their fields.

    Members nothing points at are dropped. Ties keep the declaration order, so
    the order members are declared in is part of the union's contract.

    :param payload: The raw payload.
    :param spec: The union being resolved.
    :returns: The candidate members, best first.
    :rtype: list[type[BaseModel]]
    """
    scored = [
        (-_score(payload, member, spec), position, member)
        for position, member in enumerate(spec.members)
    ]
    return [member for score, _, member in sorted(scored) if score < 0]


def _tag_error(tag: Any, spec: _UnionSpec) -> PydanticKnownError:
    """Builds the error pydantic raises for a missing or unknown tag.

    :param tag: The tag read from the payload, or ``None`` when absent.
    :param spec: The union being resolved.
    :returns: A ``union_tag_not_found`` or ``union_tag_invalid`` error.
    :rtype: PydanticKnownError
    """
    discriminator = repr(spec.discriminator)
    if tag is None:
        return PydanticKnownError(
            "union_tag_not_found", {"discriminator": discriminator}
        )
    return PydanticKnownError(
        "union_tag_invalid",
        {
            "discriminator": discriminator,
            "tag": str(tag),
            "expected_tags": ", ".join(repr(t) for t in spec.tags),
        },
    )


def _fallback(
    payload: Dict[str, Any], spec: _UnionSpec, parsing_response: bool
) -> Optional[BaseModel]:
    """Resolves a payload no member matched: to the declared fallback, then,
    only in responses, to ``SinchRawResponse``.

    :param payload: The raw payload.
    :param spec: The union being resolved.
    :param parsing_response: Whether the payload comes from the API.
    :returns: The stand-in member, or ``None`` when the payload has to be
        rejected.
    :rtype: Optional[BaseModel]
    """
    if spec.fallback is not None:
        try:
            return spec.fallback.model_validate(payload)
        except ValidationError:
            pass
    if parsing_response:
        logger.warning(
            "No member of Union[%s] matches the response payload; "
            "returning SinchRawResponse.",
            ", ".join(member.__name__ for member in spec.members),
        )
        return SinchRawResponse.model_validate(payload)
    return None


def _resolve(value: Any, spec: _UnionSpec) -> Any:
    """Resolves a raw payload to the union member it belongs to.

    :param value: The value being validated.
    :param spec: The union being resolved.
    :returns: The resolved member, or the value untouched.
    """
    if not isinstance(value, dict):
        return value

    parsing_response = _response_parsing.get()

    # If the union has a discriminator, try to resolve the member by its tag first.
    if spec.discriminator is not None:
        tag = _read_tag(value, spec)
        candidates = spec.tags.get(tag, ()) if isinstance(tag, str) else ()
        error: Optional[ValidationError] = None
        for candidate in candidates:
            try:
                return candidate.model_validate(value)
            except ValidationError as exc:
                error = exc
        # No candidate matched the tag: handle according to discriminator_strict.
        if spec.discriminator_strict:
            if not candidates:
                resolved = _fallback(value, spec, parsing_response)
                if resolved is not None:
                    return resolved
                raise _tag_error(tag, spec)
            if parsing_response:
                return _fallback(value, spec, parsing_response)
            raise error  

    # If no discriminator or the discriminator did not resolve the member, try to rank by fields instead.
    ranked = _ranked(value, spec) or list(spec.members)

    for member in ranked:
        try:
            return member.model_validate(value)
        except ValidationError:
            continue

    resolved = _fallback(value, spec, parsing_response)
    return value if resolved is None else resolved


class ResolveUnion:
    """Annotation metadata for resolving a ``Union`` it annotates.
    :param discriminator: Name of the discriminator field, if any.
    :param discriminator_strict: Whether the tag alone decides. When ``False``,
        a payload the tag does not resolve is ranked by its fields instead.
    :param fallback: Member taking the payloads no other member accepts, in
        both directions. It has to be one of the union members.
    :param tags: Explicit tag -> member(s) mapping, for members that do not
        declare their own tag.
    """

    def __init__(
        self,
        *,
        discriminator: Optional[str] = None,
        discriminator_strict: bool = True,
        fallback: Optional[Type[BaseModel]] = None,
        tags: Optional[TagMap] = None,
    ) -> None:
        self.discriminator = discriminator
        self.discriminator_strict = discriminator_strict
        self.fallback = fallback
        self.tags = tags
        self._spec: Optional[_UnionSpec] = None

    def spec_for(self, source: Any) -> _UnionSpec:
        """Builds, once, the resolution spec of the annotated union.

        :param source: The annotated type, a ``Union`` of the members.
        :returns: The spec of the union.
        :rtype: _UnionSpec
        """
        if self._spec is None:
            members = get_args(source) if get_origin(source) is Union else (source,)
            self._spec = _UnionSpec(
                tuple(m for m in members if m is not type(None)),
                self.discriminator,
                self.discriminator_strict,
                self.fallback,
                self.tags,
            )
        return self._spec

    def __get_pydantic_core_schema__(
        self, source: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        spec = self.spec_for(source)
        union_schema = handler(source)

        def resolve(value: Any, validate: Callable[[Any], Any]) -> Any:
            resolved = _resolve(value, spec)
            # A different object means _resolve already built and validated the member.
            if resolved is not value:
                return resolved
            return validate(value)

        def serialize(value: Any, serialize_member: Callable, info: Any) -> Any:
            if isinstance(value, SinchRawResponse):
                return value.model_dump(
                    mode=info.mode,
                    include=info.include,
                    exclude=info.exclude,
                    by_alias=info.by_alias,
                    exclude_unset=info.exclude_unset,
                    exclude_defaults=info.exclude_defaults,
                    exclude_none=info.exclude_none,
                )
            return serialize_member(value)

        return core_schema.no_info_wrap_validator_function(
            resolve,
            union_schema,
            serialization=core_schema.wrap_serializer_function_ser_schema(
                serialize, info_arg=True
            ),
        )
