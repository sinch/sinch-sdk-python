from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.recording_events import (
    RecordingEvents,
)


def test_recording_events_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = RecordingEvents(
        on_finish=[{"command": "hangup"}],
        on_failure=[{"command": "hangup"}],
    )

    assert isinstance(model.on_finish[0], HangupCommand)
    assert isinstance(model.on_failure[0], HangupCommand)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["onFinish"] == [{"command": "hangup"}]
    assert alias_dump["onFailure"] == [{"command": "hangup"}]


def test_recording_events_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = RecordingEvents()

    assert model.on_finish is None
    assert model.on_failure is None
