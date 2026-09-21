import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.domains.voice.models.v2.svaml.shared.message import (
    Message,
    Play,
    PlayMessage,
    Say,
    SayMessage,
)

adapter = TypeAdapter(Message)


def test_say_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = Say(text="Hello world", format="SSML", voice_name="Brian")

    assert model.text == "Hello world"
    assert model.format == "SSML"
    assert model.voice_name == "Brian"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["voiceName"] == "Brian"


def test_say_expects_optional_format_defaults_to_none():
    """Test that the optional format field defaults to None."""
    model = Say(text="Hello world", voice_name="Emma")

    assert model.format is None


def test_play_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = Play(url="https://example.com/media.mp3")

    assert model.url == "https://example.com/media.mp3"


@pytest.mark.parametrize(
    "payload, expected_model",
    [
        (
            {"type": "SAY", "say": {"text": "Hello", "voiceName": "Emma"}},
            SayMessage,
        ),
        (
            {
                "type": "PLAY",
                "play": {"url": "https://example.com/media.mp3"},
            },
            PlayMessage,
        ),
    ],
)
def test_message_expects_variant_resolved(payload, expected_model):
    """Test that each message variant of the union is resolved."""
    assert isinstance(adapter.validate_python(payload), expected_model)


def test_message_expects_validation_error_on_unknown_type():
    """Test that an unknown discriminator value is rejected."""
    with pytest.raises(ValidationError):
        adapter.validate_python({"type": "SING", "sing": {}})
