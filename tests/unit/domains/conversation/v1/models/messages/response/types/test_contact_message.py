import pytest
from pydantic import TypeAdapter

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.messages.categories.contact.contact_message import (  # noqa: E501
    ChannelSpecificContactMessage,
    ChoiceResponseContactMessage,
    FallbackContactMessage,
    LocationContactMessage,
    MediaCardContactMessage,
    MediaContactMessage,
    ProductResponseContactMessage,
    TextContactMessage,
)
from sinch.domains.conversation.models.v1.messages.response.types.contact_message import (  # noqa: E501
    ContactMessage,
)

adapter = TypeAdapter(ContactMessage)

LOCATION = {
    "title": "Sinch",
    "coordinates": {"latitude": 55.6, "longitude": 13.0},
}


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        ({"text_message": {"text": "Hello"}}, TextContactMessage),
        (
            {"media_message": {"url": "https://example.com/image.jpg"}},
            MediaContactMessage,
        ),
        (
            {
                "media_card_message": {
                    "url": "https://example.com/image.jpg",
                    "caption": "A caption",
                }
            },
            MediaCardContactMessage,
        ),
        ({"location_message": LOCATION}, LocationContactMessage),
        (
            {
                "choice_response_message": {
                    "message_id": "m1",
                    "postback_data": "chose_1",
                }
            },
            ChoiceResponseContactMessage,
        ),
        (
            {"product_response_message": {"catalog_id": "c1"}},
            ProductResponseContactMessage,
        ),
        (
            {"fallback_message": {"reason": {"description": "unsupported"}}},
            FallbackContactMessage,
        ),
        (
            {
                "channel_specific_message": {
                    "message_type": "nfm_reply",
                    "message": {
                        "type": "nfm_reply",
                        "nfm_reply": {
                            "name": "flow",
                            "response_json": "{}",
                            "body": "Sent",
                        },
                    },
                }
            },
            ChannelSpecificContactMessage,
        ),
    ],
    ids=[
        "text",
        "media",
        "media_card",
        "location",
        "choice_response",
        "product_response",
        "fallback",
        "channel_specific",
    ],
)
def test_contact_message_resolves_each_variant(payload, expected_type):
    """
    Expects each inbound contact message variant to resolve from the message
    key it declares.
    """
    with response_parsing_scope():
        message = adapter.validate_python(payload)

    assert type(message) is expected_type


def test_contact_message_resolves_to_unknown_when_a_known_key_does_not_validate():
    """
    Expects a known message key whose content does not validate to resolve to
    SinchRawResponse keeping the payload.
    """
    payload = {"location_message": {"title": "Sinch"}}
    with response_parsing_scope():
        message = adapter.validate_python(payload)

    assert isinstance(message, SinchRawResponse)
    assert message.model_dump() == payload


@pytest.mark.parametrize(
    "payload",
    [{"reaction_message": {"emoji": "thumbs_up"}}, {}],
    ids=["unknown_message_key", "no_message_key"],
)
def test_contact_message_resolves_to_the_first_variant_when_no_key_identifies_one(payload):
    """
    Expects a payload no message key identifies to resolve to the first
    declared variant keeping the payload as extras, as it always did.
    """
    with response_parsing_scope():
        message = adapter.validate_python(payload)

    assert type(message) is ChoiceResponseContactMessage
