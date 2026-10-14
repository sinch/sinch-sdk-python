from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.domains.voice.models.v2.shared.call_origin import CallOrigin
from sinch.domains.voice.models.v2.shared.phone import Phone
from sinch.domains.voice.models.v2.shared.sip_from import SipFrom

adapter = TypeAdapter(CallOrigin)


@pytest.mark.parametrize(
    "payload, expected_model",
    [
        ({"type": "PHONE", "phone": {"number": "+4673522488"}}, Phone),
        (
            {"type": "SIP", "sip": {"endpoint": "sip:user@example.com"}},
            SipFrom,
        ),
    ],
)
def test_call_origin_expects_variant_resolved(payload, expected_model):
    """Test that each origin variant of the union is resolved."""
    assert isinstance(adapter.validate_python(payload), expected_model)


def test_call_origin_expects_validation_error_on_unknown_type():
    """Test that an unknown discriminator value is rejected."""
    with pytest.raises(ValidationError):
        adapter.validate_python({"type": "STREAM", "stream": {}})


def test_call_origin_expects_unknown_type_parsed_in_a_response():
    """Test that an origin type added to the API later is parsed as
    SinchRawResponse instead of failing the whole response."""
    payload = {"type": "STREAM", "stream": {}}

    with response_parsing_scope():
        origin = adapter.validate_python(payload)

    assert isinstance(origin, SinchRawResponse)
    assert origin.model_dump() == payload
