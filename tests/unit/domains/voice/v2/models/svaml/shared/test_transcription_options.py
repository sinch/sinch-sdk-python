from sinch.domains.voice.models.v2.svaml.shared.transcription_options import (
    TranscriptionOptions,
)


def test_transcription_options_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = TranscriptionOptions(is_enabled=True, locale="en-US")

    assert model.is_enabled is True
    assert model.locale == "en-US"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["isEnabled"] is True


def test_transcription_options_expects_optional_locale_defaults_to_none():
    """Test that the optional locale field defaults to None."""
    model = TranscriptionOptions(is_enabled=True)

    assert model.locale is None
