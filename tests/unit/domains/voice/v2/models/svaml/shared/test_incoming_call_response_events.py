from sinch.domains.voice.models.v2.svaml.shared.incoming_call_response_events import (
    IncomingCallResponseEvents,
)
from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)


def test_incoming_call_response_events_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = IncomingCallResponseEvents(on_hangup=[{"command": "hangup"}])

    assert isinstance(model.on_hangup[0], HangupCommand)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["onHangup"] == [{"command": "hangup"}]


def test_incoming_call_response_events_expects_optional_on_hangup_defaults_to_none():
    """Test that the optional on_hangup field defaults to None."""
    model = IncomingCallResponseEvents()

    assert model.on_hangup is None
