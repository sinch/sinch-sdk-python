import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.sinch_events.incoming_call_events import (
    IncomingCallEvents,
)
from sinch.domains.voice.models.v2.sinch_events.voice_sinch_event_response import (
    VoiceSinchEventResponse,
)
from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)

COMMANDS = [{"command": "hangup"}]


def test_voice_sinch_event_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = VoiceSinchEventResponse(
        commands=COMMANDS,
        call_name="incoming",
        events={"on_hangup": [{"command": "hangup"}]},
    )

    assert isinstance(model.commands[0], HangupCommand)
    assert model.call_name == "incoming"
    assert isinstance(model.events, IncomingCallEvents)
    assert isinstance(model.events.on_hangup[0], HangupCommand)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["commands"] == [{"command": "hangup"}]
    assert alias_dump["callName"] == "incoming"
    assert alias_dump["events"]["onHangup"] == [{"command": "hangup"}]


def test_voice_sinch_event_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = VoiceSinchEventResponse(commands=COMMANDS)

    assert model.call_name is None
    assert model.events is None


def test_voice_sinch_event_response_expects_validation_error_for_missing_required():
    """Test that commands is required."""
    with pytest.raises(ValidationError):
        VoiceSinchEventResponse()
