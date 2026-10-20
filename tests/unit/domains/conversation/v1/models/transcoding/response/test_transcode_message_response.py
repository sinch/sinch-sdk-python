from sinch.domains.conversation.models.v1.transcoding.response.transcode_message_response import (
    TranscodeMessageResponse,
)


def test_transcode_message_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = TranscodeMessageResponse(
        transcoded_message={"SMS": "text", "WHATSAPP": "{}"}
    )

    assert model.transcoded_message == {"SMS": "text", "WHATSAPP": "{}"}

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {
        "transcoded_message": {"SMS": "text", "WHATSAPP": "{}"},
    }


def test_transcode_message_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = TranscodeMessageResponse()

    assert model.transcoded_message is None
