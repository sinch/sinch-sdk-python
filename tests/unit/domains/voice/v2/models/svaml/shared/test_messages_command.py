import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.messages_command import (
    MessagesCommand,
)

SAY_MESSAGE = {"type": "SAY", "say": {"text": "Hello", "voice_name": "Emma"}}


def test_messages_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MessagesCommand(
        command="messages",
        messages_name="greeting-sequence",
        messages=[SAY_MESSAGE],
        events={"on_finish": [{"command": "hangup"}]},
    )

    assert model.command == "messages"
    assert model.messages_name == "greeting-sequence"
    assert model.messages[0].say.text == "Hello"
    assert model.events.on_finish[0].command == "hangup"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["messagesName"] == "greeting-sequence"


def test_messages_command_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = MessagesCommand(command="messages", messages=[SAY_MESSAGE])

    assert model.messages_name is None
    assert model.events is None


def test_messages_command_expects_validation_error_for_missing_required():
    """Test that messages is required."""
    with pytest.raises(ValidationError):
        MessagesCommand(command="messages")
