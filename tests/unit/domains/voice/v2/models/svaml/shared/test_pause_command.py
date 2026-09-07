import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.pause_command import PauseCommand


def test_pause_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = PauseCommand(command="pause", duration_milliseconds=1500)

    assert model.command == "pause"
    assert model.duration_milliseconds == 1500

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["durationMilliseconds"] == 1500


def test_pause_command_expects_validation_error_for_missing_required():
    """Test that duration_milliseconds is required."""
    with pytest.raises(ValidationError):
        PauseCommand(command="pause")
