import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.sms.models.v1.shared.mo_binary_message import (
    MOBinaryMessage,
)
from sinch.domains.sms.models.v1.shared.mo_media_message import MOMediaMessage
from sinch.domains.sms.models.v1.shared.mo_text_message import MOTextMessage
from sinch.domains.sms.models.v1.types.inbound_message import InboundMessage

adapter = TypeAdapter(InboundMessage)

COMMON = {
    "id": "01FC66621XXXXX119Z8PMV1QPQ",
    "from": "+12017777777",
    "to": "+12018888888",
    "received_at": "2024-01-15T14:30:22.123Z",
}


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        ({**COMMON, "type": "mo_text", "body": "Hello"}, MOTextMessage),
        (
            {**COMMON, "type": "mo_binary", "body": "SGVsbG8=", "udh": "0605"},
            MOBinaryMessage,
        ),
        (
            {
                **COMMON,
                "type": "mo_media",
                "body": {"url": "https://example.com/image.jpg"},
            },
            MOMediaMessage,
        ),
    ],
    ids=["text", "binary", "media"],
)
def test_inbound_message_resolves_each_variant(payload, expected_type):
    """
    Expects each inbound message variant to resolve from its type field.
    """
    with response_parsing_scope():
        message = adapter.validate_python(payload)

    assert type(message) is expected_type


def test_inbound_message_resolves_an_unknown_type_to_unknown():
    """
    Expects an inbound type added to the API later to be parsed as
    SinchRawResponse, keeping the payload, instead of failing the whole callback.
    """
    payload = {**COMMON, "type": "mo_future", "body": "Hello"}

    with response_parsing_scope():
        message = adapter.validate_python(payload)

    assert isinstance(message, SinchRawResponse)
    assert message.model_dump() == payload


def test_inbound_message_rejects_an_unknown_type_outside_a_response():
    """
    Expects the same payload to be rejected when it is not being parsed from a
    response, since only the API is allowed to introduce new variants.
    """
    with pytest.raises(ValidationError, match="does not match any of the expected tags"):
        adapter.validate_python({**COMMON, "type": "mo_future"})
