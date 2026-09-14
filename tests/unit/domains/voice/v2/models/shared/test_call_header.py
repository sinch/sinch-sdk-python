from sinch.domains.voice.models.v2.shared.call_header import CallHeader


def test_call_header_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = CallHeader(key="headerKey", value="headerValue")

    assert model.key == "headerKey"
    assert model.value == "headerValue"


def test_call_header_expects_optional_value_defaults_to_none():
    """Test that the optional value field defaults to None."""
    model = CallHeader(key="headerKey")

    assert model.value is None
