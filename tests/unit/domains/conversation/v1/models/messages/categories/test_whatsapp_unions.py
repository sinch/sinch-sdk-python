import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_boleto_button import (  # noqa: E501
    WhatsAppPaymentSettingsBoletoButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_payment_link_button import (  # noqa: E501
    WhatsAppPaymentSettingsPaymentLinkButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_pix_button import (  # noqa: E501
    WhatsAppPaymentSettingsPixButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_document_header import (  # noqa: E501
    WhatsAppInteractiveDocumentHeader,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_image_header import (  # noqa: E501
    WhatsAppInteractiveImageHeader,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_text_header import (  # noqa: E501
    WhatsAppInteractiveTextHeader,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.whatsapp_interactive_video_header import (  # noqa: E501
    WhatsAppInteractiveVideoHeader,
)
from sinch.domains.conversation.models.v1.messages.response.types.whatsapp_interactive_header import (  # noqa: E501
    WhatsAppInteractiveHeader,
)
from sinch.domains.conversation.models.v1.messages.response.types.whatsapp_payment_button import (  # noqa: E501
    WhatsAppPaymentButton,
)

header_adapter = TypeAdapter(WhatsAppInteractiveHeader)
button_adapter = TypeAdapter(WhatsAppPaymentButton)

MEDIA = {"link": "https://example.com/file"}


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        ({"type": "text", "text": "A header"}, WhatsAppInteractiveTextHeader),
        ({"type": "image", "image": MEDIA}, WhatsAppInteractiveImageHeader),
        (
            {"type": "document", "document": MEDIA},
            WhatsAppInteractiveDocumentHeader,
        ),
        ({"type": "video", "video": MEDIA}, WhatsAppInteractiveVideoHeader),
    ],
    ids=["text", "image", "document", "video"],
)
def test_whatsapp_interactive_header_resolves_each_variant(
    payload, expected_type
):
    """
    Expects each interactive header variant to resolve from its type field.
    """
    assert type(header_adapter.validate_python(payload)) is expected_type


def test_whatsapp_interactive_header_unknown_type_is_unknown_in_a_response():
    """
    Expects a header type added to the API later to be parsed as SinchRawResponse
    instead of failing the whole message.
    """
    payload = {"type": "audio", "audio": MEDIA}

    with response_parsing_scope():
        header = header_adapter.validate_python(payload)

    assert isinstance(header, SinchRawResponse)
    assert header.model_dump() == payload


def test_whatsapp_interactive_header_rejects_an_unknown_type_in_a_request():
    """
    Expects the same header type to be rejected when building a message.
    """
    with pytest.raises(ValidationError, match="does not match any of the expected tags"):
        header_adapter.validate_python({"type": "audio", "audio": MEDIA})


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        (
            {
                "type": "pix_dynamic_code",
                "code": "code-1",
                "merchant_name": "Acme",
                "key": "key-1",
                "key_type": "CPF",
            },
            WhatsAppPaymentSettingsPixButton,
        ),
        (
            {"type": "payment_link", "uri": "https://example.com/pay"},
            WhatsAppPaymentSettingsPaymentLinkButton,
        ),
        (
            {"type": "boleto", "digitable_line": "0001"},
            WhatsAppPaymentSettingsBoletoButton,
        ),
    ],
    ids=["pix", "payment_link", "boleto"],
)
def test_whatsapp_payment_button_resolves_each_variant(payload, expected_type):
    """
    Expects each payment button variant to resolve from the fields it declares.
    """
    assert type(button_adapter.validate_python(payload)) is expected_type
