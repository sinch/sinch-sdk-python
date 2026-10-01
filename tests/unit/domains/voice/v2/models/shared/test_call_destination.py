from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.domains.voice.models.v2.shared.call_destination import (
    CallDestination,
)
from sinch.domains.voice.models.v2.shared.phone import Phone
from sinch.domains.voice.models.v2.shared.sip import Sip
from sinch.domains.voice.models.v2.shared.stream import Stream
from sinch.domains.voice.models.v2.shared.voice_relay import VoiceRelay

adapter = TypeAdapter(CallDestination)


@pytest.mark.parametrize(
    "payload, expected_model",
    [
        ({"type": "PHONE", "phone": {"number": "+4673522488"}}, Phone),
        (
            {"type": "SIP", "sip": {"endpoint": "sips:user@example.com"}},
            Sip,
        ),
        (
            {"type": "STREAM", "stream": {"endpoint": "wss://example.com"}},
            Stream,
        ),
        (
            {
                "type": "VOICE_RELAY",
                "voiceRelay": {
                    "endpoint": "wss://acme.com/agent",
                    "ttsVoice": "Emma",
                    "sttLanguage": "en-US",
                },
            },
            VoiceRelay,
        ),
    ],
)
def test_call_destination_expects_variant_resolved(payload, expected_model):
    """Test that each destination variant of the union is resolved."""
    assert isinstance(adapter.validate_python(payload), expected_model)


def test_call_destination_expects_validation_error_on_unknown_type():
    """Test that an unknown discriminator value is rejected."""
    with pytest.raises(ValidationError):
        adapter.validate_python({"type": "FAX", "fax": {}})


def test_call_destination_expects_unknown_type_parsed_in_a_response():
    """Test that a destination type added to the API later is parsed as
    SinchRawResponse instead of failing the whole response."""
    payload = {"type": "FAX", "fax": {}}

    with response_parsing_scope():
        destination = adapter.validate_python(payload)

    assert isinstance(destination, SinchRawResponse)
    assert destination.model_dump() == payload
