from sinch.domains.voice.models.v2.svaml.shared.amd_events import AmdEvents
from sinch.domains.voice.models.v2.svaml.shared.answer_command import (
    AnswerCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)


def test_amd_events_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = AmdEvents(
        on_human=[{"command": "answer"}],
        on_machine=[{"command": "hangup"}],
        on_beep=[{"command": "hangup"}],
        on_unknown=[{"command": "hangup"}],
    )

    assert isinstance(model.on_human[0], AnswerCommand)
    assert isinstance(model.on_machine[0], HangupCommand)
    assert isinstance(model.on_beep[0], HangupCommand)
    assert isinstance(model.on_unknown[0], HangupCommand)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["onHuman"] == [{"command": "answer"}]
    assert alias_dump["onUnknown"] == [{"command": "hangup"}]


def test_amd_events_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = AmdEvents()

    assert model.on_human is None
    assert model.on_machine is None
    assert model.on_beep is None
    assert model.on_unknown is None
