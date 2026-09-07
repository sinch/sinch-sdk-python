import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.stop_recording_command import (
    StopRecordingCommand,
)


def test_stop_recording_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StopRecordingCommand(
        command="stopRecording", recording_name="my-recording"
    )

    assert model.command == "stopRecording"
    assert model.recording_name == "my-recording"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["recordingName"] == "my-recording"


def test_stop_recording_command_expects_validation_error_for_missing_required():
    """Test that recording_name is required."""
    with pytest.raises(ValidationError):
        StopRecordingCommand(command="stopRecording")
