import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.start_recording_command import (
    StartRecordingCommand,
)

RECORDING_OPTIONS = {
    "destination": "AWS",
    "destination_url": "s3://bucket/calls",
    "credentials": "secret",
}


def test_start_recording_command_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StartRecordingCommand(
        command="startRecording",
        recording_name="customer-support-recording",
        recording_options=RECORDING_OPTIONS,
        events={"on_failure": [{"command": "hangup"}]},
    )

    assert model.command == "startRecording"
    assert model.recording_name == "customer-support-recording"
    assert model.recording_options.destination == "AWS"
    assert model.events.on_failure[0].command == "hangup"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["recordingName"] == "customer-support-recording"
    assert alias_dump["recordingOptions"]["destination"] == "AWS"


def test_start_recording_command_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = StartRecordingCommand(
        command="startRecording", recording_options=RECORDING_OPTIONS
    )

    assert model.recording_name is None
    assert model.events is None


def test_start_recording_command_expects_validation_error_for_missing_required():
    """Test that recording_options is required."""
    with pytest.raises(ValidationError):
        StartRecordingCommand(command="startRecording")
