from sinch.domains.voice.models.v2.shared.sip import Sip, SipDetails


def test_sip_details_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SipDetails(
        endpoint="sip:user@example.com",
        transport="TCP",
        call_headers=[{"key": "X-Correlation-Id", "value": "12345"}],
    )

    assert model.endpoint == "sip:user@example.com"
    assert model.transport == "TCP"
    assert model.call_headers[0].key == "X-Correlation-Id"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["callHeaders"] == [
        {"key": "X-Correlation-Id", "value": "12345"}
    ]


def test_sip_details_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = SipDetails(endpoint="sip:user@example.com")

    assert model.transport is None
    assert model.call_headers is None


def test_sip_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = Sip(
        type="SIP",
        sip={
            "endpoint": "sip:user@example.com",
            "transport": "TLS",
            "call_headers": [{"key": "X-Correlation-Id", "value": "12345"}],
        },
    )

    assert model.type == "SIP"
    assert model.sip.endpoint == "sip:user@example.com"
    assert model.sip.transport == "TLS"
    assert model.sip.call_headers[0].key == "X-Correlation-Id"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["sip"]["callHeaders"] == [
        {"key": "X-Correlation-Id", "value": "12345"}
    ]
