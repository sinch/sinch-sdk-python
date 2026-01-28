from typing import Annotated, Union, get_args
from pydantic import BeforeValidator

from sinch.domains.conversation.models.v1.messages.categories.choice.choice_options import (
    CalendarChoiceMessage,
    CallChoiceMessage,
    ChoiceMessageWithPostback,
    LocationChoiceMessage,
    ShareLocationChoiceMessage,
    TextChoiceMessage,
    UrlChoiceMessage,
)

ChoiceOptionUnion = Union[
    CallChoiceMessage,
    LocationChoiceMessage,
    TextChoiceMessage,
    UrlChoiceMessage,
    CalendarChoiceMessage,
    ShareLocationChoiceMessage,
]


def _choice_message_type_keys() -> frozenset[str]:
    """Message-type keys derived from Union members (spec: choiceTypes oneOf)."""
    base_fields = set(ChoiceMessageWithPostback.model_fields)
    keys = set()
    for model in get_args(ChoiceOptionUnion):
        keys.update(model.model_fields.keys() - base_fields)
    return frozenset(keys)


_CHOICE_MESSAGE_TYPE_KEYS = _choice_message_type_keys()


def _validate_exactly_one_choice_message_key(value: object) -> object:
    """Ensure each choice dict has exactly one message-type key."""
    if not isinstance(value, dict):
        return value
    keys = _CHOICE_MESSAGE_TYPE_KEYS
    count = sum(1 for k in keys if value.get(k) is not None)
    if count != 1:
        raise ValueError(
            f"Each choice must have exactly one of: {', '.join(sorted(keys))}."
        )
    return value


ChoiceOption = Annotated[
    ChoiceOptionUnion,
    BeforeValidator(_validate_exactly_one_choice_message_key),
]
