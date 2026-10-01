import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.domains.conversation.models.v1.messages.categories.choice.choice_option import (  # noqa: E501
    ChoiceOption,
)
from sinch.domains.conversation.models.v1.messages.categories.choice.choice_options import (  # noqa: E501
    CalendarChoiceMessage,
    CallChoiceMessage,
    LocationChoiceMessage,
    ShareLocationChoiceMessage,
    TextChoiceMessage,
    UrlChoiceMessage,
)

adapter = TypeAdapter(ChoiceOption)


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        (
            {"call_message": {"phone_number": "+12017777777", "title": "Call"}},
            CallChoiceMessage,
        ),
        ({"text_message": {"text": "Yes"}}, TextChoiceMessage),
        (
            {"url_message": {"title": "Open", "url": "https://example.com"}},
            UrlChoiceMessage,
        ),
        (
            {
                "calendar_message": {
                    "title": "Book",
                    "event_start": "2026-01-15T14:00:00Z",
                    "event_end": "2026-01-15T15:00:00Z",
                    "event_title": "A meeting",
                    "fallback_url": "https://example.com",
                }
            },
            CalendarChoiceMessage,
        ),
        (
            {
                "location_message": {
                    "title": "Sinch",
                    "coordinates": {"latitude": 55.6, "longitude": 13.0},
                }
            },
            LocationChoiceMessage,
        ),
        (
            {
                "share_location_message": {
                    "title": "Share",
                    "fallback_url": "https://example.com",
                }
            },
            ShareLocationChoiceMessage,
        ),
    ],
    ids=["call", "text", "url", "calendar", "location", "share_location"],
)
def test_choice_option_resolves_each_variant(payload, expected_type):
    """
    Expects each choice variant to resolve from the message key it declares.
    """
    assert type(adapter.validate_python(payload)) is expected_type


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"text_message": {"text": "Yes"}, "url_message": {"title": "Open"}},
        {"reaction_message": {"emoji": "thumbs_up"}},
    ],
    ids=["no_message_key", "two_message_keys", "unknown_message_key"],
)
def test_choice_option_requires_exactly_one_message_key(payload):
    """
    Expects a choice carrying none, several, or an unrecognized message key to
    be rejected in both directions: the check runs ahead of the resolution, so
    this union does not fall back to SinchRawResponse while parsing a response.
    """
    with pytest.raises(ValidationError, match="Each choice must have"):
        adapter.validate_python(payload)
