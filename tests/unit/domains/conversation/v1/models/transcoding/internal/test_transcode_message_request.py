import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.transcoding.internal.transcode_message_request import (
    TranscodeMessageRequest,
)


def test_transcode_message_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = TranscodeMessageRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        app_message={"text_message": {"text": "Hello"}},
        channels=["SMS", "WHATSAPP"],
        from_="sender",
        to="recipient",
    )

    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.app_message.text_message.text == "Hello"
    assert model.channels == ["SMS", "WHATSAPP"]
    assert model.from_ == "sender"
    assert model.to == "recipient"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "app_message": {"text_message": {"text": "Hello"}},
        "channels": ["SMS", "WHATSAPP"],
        "from": "sender",
        "to": "recipient",
    }


def test_transcode_message_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = TranscodeMessageRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        app_message={"text_message": {"text": "Hello"}},
        channels=["SMS"],
    )

    assert model.from_ is None
    assert model.to is None


def test_transcode_message_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        TranscodeMessageRequest(
            app_message={"text_message": {"text": "Hello"}},
            channels=["SMS"],
        )
