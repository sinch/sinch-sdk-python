import pytest
from pydantic import TypeAdapter

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.messages.categories.app.app_message import (  # noqa: E501
    CardAppMessage,
    CarouselAppMessage,
    ChoiceAppMessage,
    ContactInfoAppMessage,
    ListAppMessage,
    LocationAppMessage,
    MediaAppMessage,
    TemplateAppMessage,
    TextAppMessage,
)
from sinch.domains.conversation.models.v1.messages.response.types.app_message import (  # noqa: E501
    AppMessage,
)

adapter = TypeAdapter(AppMessage)

LOCATION = {
    "title": "Sinch",
    "coordinates": {"latitude": 55.6, "longitude": 13.0},
}


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        ({"text_message": {"text": "Hello"}}, TextAppMessage),
        ({"card_message": {"title": "A card"}}, CardAppMessage),
        ({"carousel_message": {"cards": []}}, CarouselAppMessage),
        ({"choice_message": {"choices": []}}, ChoiceAppMessage),
        (
            {
                "contact_info_message": {
                    "name": {"full_name": "Jane Doe"},
                    "phone_numbers": [{"phone_number": "+12017777777"}],
                }
            },
            ContactInfoAppMessage,
        ),
        (
            {"list_message": {"title": "A list", "sections": []}},
            ListAppMessage,
        ),
        ({"location_message": LOCATION}, LocationAppMessage),
        (
            {"media_message": {"url": "https://example.com/image.jpg"}},
            MediaAppMessage,
        ),
        (
            {
                "template_message": {
                    "omni_template": {"template_id": "t1", "version": "1"}
                }
            },
            TemplateAppMessage,
        ),
    ],
    ids=[
        "text",
        "card",
        "carousel",
        "choice",
        "contact_info",
        "list",
        "location",
        "media",
        "template",
    ],
)
def test_app_message_resolves_each_variant(payload, expected_type):
    """
    Expects each app message variant to resolve from the message key it
    declares, whatever its position in the union.
    """
    with response_parsing_scope():
        message = adapter.validate_python(payload)

    assert type(message) is expected_type


def test_app_message_resolves_to_unknown_when_a_known_key_does_not_validate():
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
def test_app_message_resolves_to_the_first_variant_when_no_key_identifies_one(payload):
    """
    Expects a payload no message key identifies to resolve to the first
    declared variant keeping the payload as extras, as it always did.
    """
    with response_parsing_scope():
        message = adapter.validate_python(payload)

    assert type(message) is CardAppMessage


def test_app_message_breaks_two_message_keys_by_declaration_order():
    """
    Expects a payload carrying two message keys to resolve to the variant
    declared first, which is the union's documented tie-break.
    """
    payload = {
        "text_message": {"text": "Hello"},
        "location_message": LOCATION,
    }
    with response_parsing_scope():
        message = adapter.validate_python(payload)

    assert type(message) is LocationAppMessage
