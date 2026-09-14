from sinch.domains.voice.models.v2.shared.sip_from import (
    SipFrom,
    SipFromDetails,
)


def test_sip_from_details_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SipFromDetails(
        endpoint="sip:user@example.com", display_name="Alice"
    )

    assert model.endpoint == "sip:user@example.com"
    assert model.display_name == "Alice"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["displayName"] == "Alice"


def test_sip_from_details_expects_optional_display_name_defaults_to_none():
    """Test that the optional display_name field defaults to None."""
    model = SipFromDetails(endpoint="sip:user@example.com")

    assert model.display_name is None


def test_sip_from_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SipFrom(
        type="SIP",
        sip={"endpoint": "sip:user@example.com", "display_name": "Alice"},
    )

    assert model.type == "SIP"
    assert model.sip.endpoint == "sip:user@example.com"
    assert model.sip.display_name == "Alice"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["sip"]["displayName"] == "Alice"
