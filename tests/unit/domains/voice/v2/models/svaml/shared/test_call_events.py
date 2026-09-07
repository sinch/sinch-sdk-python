from sinch.domains.voice.models.v2.svaml.shared.answer_command import (
    AnswerCommand,
)
from sinch.domains.voice.models.v2.svaml.shared.call_events import CallEvents
from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)


def test_call_events_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = CallEvents(
        on_answer=[{"command": "answer"}],
        on_busy=[{"command": "hangup"}],
        on_reject=[{"command": "hangup"}],
        on_timeout=[{"command": "hangup"}],
        on_hangup=[{"command": "hangup"}],
        on_failure=[{"command": "hangup"}],
    )

    assert isinstance(model.on_answer[0], AnswerCommand)
    assert isinstance(model.on_busy[0], HangupCommand)
    assert isinstance(model.on_reject[0], HangupCommand)
    assert isinstance(model.on_timeout[0], HangupCommand)
    assert isinstance(model.on_hangup[0], HangupCommand)
    assert isinstance(model.on_failure[0], HangupCommand)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["onAnswer"] == [{"command": "answer"}]
    assert alias_dump["onFailure"] == [{"command": "hangup"}]


def test_call_events_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = CallEvents()

    assert model.on_answer is None
    assert model.on_busy is None
    assert model.on_reject is None
    assert model.on_timeout is None
    assert model.on_hangup is None
    assert model.on_failure is None
