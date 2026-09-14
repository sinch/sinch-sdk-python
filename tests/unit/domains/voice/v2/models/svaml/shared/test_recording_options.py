import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.svaml.shared.recording_options import (
    RecordingOptions,
)


@pytest.mark.parametrize(
    "destination", ["AWS", "GCP", "AZURE", "UNEXPECTED_VALUE"]
)
def test_recording_options_expects_parsed_input(destination):
    """Test that the model correctly parses a full valid input."""
    model = RecordingOptions(
        format="MP3",
        recording_type="COMBINED",
        destination=destination,
        destination_url="s3://voice-recordings-prod/calls",
        credentials="accessKeyId:secretAccessKey:eu-central-1",
        transcription_options={"is_enabled": True, "locale": "en-US"},
    )

    assert model.format == "MP3"
    assert model.recording_type == "COMBINED"
    assert model.destination == destination
    assert model.destination_url == "s3://voice-recordings-prod/calls"
    assert model.credentials == "accessKeyId:secretAccessKey:eu-central-1"
    assert model.transcription_options.is_enabled is True

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["recordingType"] == "COMBINED"
    assert alias_dump["destinationUrl"] == "s3://voice-recordings-prod/calls"
    assert alias_dump["transcriptionOptions"]["isEnabled"] is True


def test_recording_options_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = RecordingOptions(
        destination="AWS",
        destination_url="s3://bucket/calls",
        credentials="secret",
    )

    assert model.format is None
    assert model.recording_type is None
    assert model.transcription_options is None


def test_recording_options_expects_validation_error_for_missing_required():
    """Test that destination, destination_url and credentials are required."""
    with pytest.raises(ValidationError):
        RecordingOptions()
