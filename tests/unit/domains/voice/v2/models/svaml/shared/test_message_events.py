from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.message_events import (
    MessageEvents,
)


def test_message_events_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MessageEvents(
        on_finish=[{"command": "hangup"}],
    )

    assert isinstance(model.on_finish[0], HangupCommand)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["onFinish"] == [{"command": "hangup"}]


def test_message_events_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = MessageEvents()

    assert model.on_finish is None
