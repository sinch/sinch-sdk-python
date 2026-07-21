import pytest
from sinch.domains.conversation.models.v1.messages.categories.card.card_message import (
    CardMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.carousel.carousel_message import (
    CarouselMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.choice.choice_message import (
    ChoiceMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.choice.choice_options import (
    TextChoiceMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.location.location_message import (
    LocationMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.media import (
    MediaProperties,
)
from sinch.domains.conversation.models.v1.messages.categories.template import (
    TemplateMessage,
    TemplateReferenceOmniChannel,
)
from sinch.domains.conversation.models.v1.messages.categories.text import (
    TextMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.request import (
    SendMessageRequestBody,
)
from sinch.domains.conversation.models.v1.messages.shared.coordinates import (
    Coordinates,
)


def test_send_message_request_body_expects_accepts_text_message():
    """
    Test that the model accepts text_message with valid content.
    """
    body = SendMessageRequestBody(text_message=TextMessage(text="Test message content"))

    assert body.text_message.text == "Test message content"


def test_send_message_request_body_expects_accepts_card_message():
    """
    Test that the model accepts card_message.
    """
    body = SendMessageRequestBody(card_message=CardMessage(title="Card title"))

    assert body.card_message is not None
    assert body.card_message.title == "Card title"


def test_send_message_request_body_expects_accepts_carousel_message():
    """
    Test that the model accepts carousel_message with a list of cards.
    """
    body = SendMessageRequestBody(
        carousel_message=CarouselMessage(cards=[CardMessage(title="Card 1")])
    )

    assert body.carousel_message is not None
    assert len(body.carousel_message.cards) == 1
    assert body.carousel_message.cards[0].title == "Card 1"


def test_send_message_request_body_expects_accepts_choice_message():
    """
    Test that the model accepts choice_message with choices.
    """
    body = SendMessageRequestBody(
        choice_message=ChoiceMessage(
            choices=[TextChoiceMessage(text_message=TextMessage(text="Option 1"))]
        )
    )

    assert body.choice_message is not None
    assert len(body.choice_message.choices) == 1
    assert body.choice_message.choices[0].text_message.text == "Option 1"


def test_send_message_request_body_expects_accepts_location_message():
    """
    Test that the model accepts location_message with coordinates and title.
    """
    body = SendMessageRequestBody(
        location_message=LocationMessage(
            coordinates=Coordinates(latitude=59.3293, longitude=18.0686),
            title="Stockholm",
        )
    )

    assert body.location_message is not None
    assert body.location_message.title == "Stockholm"
    assert body.location_message.coordinates.latitude == 59.3293
    assert body.location_message.coordinates.longitude == 18.0686


def test_send_message_request_body_expects_accepts_media_message():
    """
    Test that the model accepts media_message with url.
    """
    body = SendMessageRequestBody(
        media_message=MediaProperties(url="https://example.com/image.jpg")
    )

    assert body.media_message is not None
    assert body.media_message.url == "https://example.com/image.jpg"


def test_send_message_request_body_expects_accepts_template_message():
    """
    Test that the model accepts template_message with omni_template.
    """
    body = SendMessageRequestBody(
        template_message=TemplateMessage(
            omni_template=TemplateReferenceOmniChannel(
                template_id="tpl_123", version="latest"
            )
        )
    )

    assert body.template_message is not None
    assert body.template_message.omni_template is not None
    assert body.template_message.omni_template.template_id == "tpl_123"
    assert body.template_message.omni_template.version == "latest"


def test_send_message_request_body_expects_accepts_choice_with_one_message_key():
    """
    Parsing from dict: each choice with exactly one message-type key is valid.
    Choices array can include Call, Location, Text, URL, Calendar, Request location
    (number limited to 10 per spec).
    """
    choices = [
        {"text_message": {"text": "Option 1"}},
        {"call_message": {"title": "Call us", "phone_number": "+46732000000"}},
        {"url_message": {"title": "Website", "url": "https://example.com"}},
        {
            "location_message": {
                "title": "Show map",
                "coordinates": {"latitude": 59.33, "longitude": 18.07},
            }
        },
        {
            "share_location_message": {
                "title": "Share location",
                "fallback_url": "https://example.com",
            }
        },
    ]
    body = SendMessageRequestBody(
        choice_message=ChoiceMessage(choices=choices)
    )
    assert body.choice_message is not None
    assert len(body.choice_message.choices) == 5
    assert body.choice_message.choices[0].text_message.text == "Option 1"
    assert body.choice_message.choices[1].call_message.phone_number == "+46732000000"
    assert body.choice_message.choices[2].url_message.url == "https://example.com"
    assert body.choice_message.choices[3].location_message.title == "Show map"
    assert (
        body.choice_message.choices[4].share_location_message.title
        == "Share location"
    )


def test_send_message_request_body_expects_rejects_choice_with_zero_message_keys():
    """
    Parsing from dict: choice with no message-type key raises.
    """
    with pytest.raises(ValueError, match="exactly one of"):
        SendMessageRequestBody(
            choice_message=ChoiceMessage(choices=[{"postback_data": "x"}])
        )


def test_send_message_request_body_expects_rejects_choice_with_two_message_keys():
    """
    Parsing from dict: choice with two message-type keys raises.
    """
    with pytest.raises(ValueError, match="exactly one of"):
        SendMessageRequestBody(
            choice_message=ChoiceMessage(
                choices=[
                    {
                        "text_message": {"text": "A"},
                        "call_message": {"title": "Call", "phone_number": "1"},
                    }
                ]
            )
        )
