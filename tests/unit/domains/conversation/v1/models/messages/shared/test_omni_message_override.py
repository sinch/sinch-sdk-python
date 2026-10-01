import pytest
from pydantic import TypeAdapter

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.domains.conversation.models.v1.messages.shared.override.omni_message_override import (  # noqa: E501
    OmniMessageOverride,
)

adapter = TypeAdapter(OmniMessageOverride)

LOCATION = {
    "title": "Sinch",
    "coordinates": {"latitude": 55.6, "longitude": 13.0},
}


@pytest.mark.parametrize(
    "payload, expected_name",
    [
        ({"text_message": {"text": "Hello"}}, "TextMessageField"),
        (
            {"media_message": {"url": "https://example.com/image.jpg"}},
            "MediaMessageField",
        ),
        (
            {"template_reference": {"template_id": "t1", "version": "1"}},
            "TemplateReferenceField",
        ),
        ({"choice_message": {"choices": []}}, "ChoiceMessageField"),
        ({"card_message": {"title": "A card"}}, "CardMessageField"),
        ({"carousel_message": {"cards": []}}, "CarouselMessageField"),
        ({"location_message": LOCATION}, "LocationMessageField"),
        (
            {
                "contact_info_message": {
                    "name": {"full_name": "Jane Doe"},
                    "phone_numbers": [{"phone_number": "+12017777777"}],
                }
            },
            "ContactInfoMessageField",
        ),
        (
            {"list_message": {"title": "A list", "sections": []}},
            "ListMessageField",
        ),
    ],
    ids=[
        "text",
        "media",
        "template_reference",
        "choice",
        "card",
        "carousel",
        "location",
        "contact_info",
        "list",
    ],
)
def test_omni_message_override_resolves_each_variant(payload, expected_name):
    """
    Expects each channel override to resolve from the message key it declares.
    """
    with response_parsing_scope():
        override = adapter.validate_python(payload)

    assert type(override).__name__ == expected_name


def test_omni_message_override_resolves_an_unknown_type_to_the_first_variant():
    """
    Expects an override type added to the API later to resolve to the first
    declared variant keeping the payload as extras, as it always did.
    """
    payload = {"reaction_message": {"emoji": "thumbs_up"}}

    with response_parsing_scope():
        override = adapter.validate_python(payload)

    assert type(override).__name__ == "TextMessageField"
    assert override.model_dump(exclude_unset=True) == payload
