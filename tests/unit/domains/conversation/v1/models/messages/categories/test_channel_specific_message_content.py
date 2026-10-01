import pytest
from pydantic import TypeAdapter

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.channel_specific_message_content import (  # noqa: E501
    ChannelSpecificMessageContent,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_carousel_commerce_channel_specific_message import (  # noqa: E501
    KakaoTalkCarouselCommerceChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_commerce_channel_specific_message import (  # noqa: E501
    KakaoTalkCommerceChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.line.line_notification_message_template_message import (  # noqa: E501
    LineNotificationMessageTemplateMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.flow_channel_specific_message import (  # noqa: E501
    FlowChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_details_channel_specific_message import (  # noqa: E501
    PaymentOrderDetailsChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_status_channel_specific_message import (  # noqa: E501
    PaymentOrderStatusChannelSpecificMessage,
)

adapter = TypeAdapter(ChannelSpecificMessageContent)

PAYMENT_ORDER_DETAILS = {
    "type": "br",
    "reference_id": "ref-1",
    "type_of_goods": "digital-goods",
    "total_amount_value": 1000,
    "order": {
        "items": [],
        "subtotal_value": 1000,
        "tax_value": 0,
    },
}
PAYMENT_ORDER_STATUS = {
    "reference_id": "ref-1",
    "order": {"status": "pending"},
}
KAKAOTALK_COMMERCE = {
    "buttons": [{"name": "Shop", "link_mo": "https://m.example.com"}],
    "image": {"image_url": "https://example.com/image.jpg"},
    "commerce": {"title": "A product", "regular_price": 1000},
}


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        (
            {"flow_id": "f1", "flow_cta": "Open"},
            FlowChannelSpecificMessage,
        ),
        (
            {"payment": PAYMENT_ORDER_DETAILS},
            PaymentOrderDetailsChannelSpecificMessage,
        ),
        (
            {"payment": PAYMENT_ORDER_STATUS},
            PaymentOrderStatusChannelSpecificMessage,
        ),
        (KAKAOTALK_COMMERCE, KakaoTalkCommerceChannelSpecificMessage),
        (
            {"carousel": {"list": []}},
            KakaoTalkCarouselCommerceChannelSpecificMessage,
        ),
        (
            {"template_key": "t1"},
            LineNotificationMessageTemplateMessage,
        ),
    ],
    ids=[
        "whatsapp_flow",
        "payment_order_details",
        "payment_order_status",
        "kakaotalk_commerce",
        "kakaotalk_carousel_commerce",
        "line_notification_template",
    ],
)
def test_channel_specific_message_content_resolves_each_variant(
    payload, expected_type
):
    """
    Expects each channel specific message to resolve from the fields it
    declares, including the two payment variants that share the same key and
    are told apart by their content.
    """
    assert type(adapter.validate_python(payload)) is expected_type


def test_channel_specific_message_content_unknown_is_unknown_in_a_response():
    """
    Expects a channel specific message added to the API later to be parsed as
    SinchRawResponse instead of failing the whole message.
    """
    payload = {"sticker": {"sticker_id": "s1"}}

    with response_parsing_scope():
        message = adapter.validate_python(payload)

    assert isinstance(message, SinchRawResponse)
    assert message.model_dump() == payload
