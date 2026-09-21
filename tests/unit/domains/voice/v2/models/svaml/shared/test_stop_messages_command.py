import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.stop_messages_command import (
    StopMessagesCommand,
)


def test_stop_messages_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StopMessagesCommand(
        command="stopMessages",
        messages_name="my-messages",
    )

    assert model.command == "stopMessages"
    assert model.messages_name == "my-messages"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["messagesName"] == "my-messages"


def test_stop_messages_command_expects_validation_error_for_missing_required():
    """Test that messages_name is required."""
    with pytest.raises(ValidationError):
        StopMessagesCommand(command="stopMessages")
