import pytest
from pydantic import ValidationError
from sinch.domains.conversation.models.v1.messages.internal.request import (
    UpdateMessageMetadataRequest,
)


@pytest.mark.parametrize("messages_source", ["CONVERSATION_SOURCE", "DISPATCH_SOURCE"])
def test_update_message_metadata_request_expects_accepts_messages_source(messages_source):
    """
    Test that the model accepts messages_source with different values.
    """
    request = UpdateMessageMetadataRequest(
        message_id="CAPY123456789ABCDEFGHIJKLMNOP",
        metadata="test_metadata",
        messages_source=messages_source
    )

    assert request.message_id == "CAPY123456789ABCDEFGHIJKLMNOP"
    assert request.metadata == "test_metadata"
    assert request.messages_source == messages_source


def test_update_message_metadata_request_expects_validation_error_for_missing_message_id():
    """
    Test that the model raises a ValidationError when message_id field is missing.
    """
    data = {
        "metadata": "test_metadata"
    }

    with pytest.raises(ValidationError) as excinfo:
        UpdateMessageMetadataRequest(**data)

    error_message = str(excinfo.value)

    assert "Field required" in error_message or "field required" in error_message
    assert "messageId" in error_message or "message_id" in error_message


def test_update_message_metadata_request_expects_validation_error_for_missing_metadata():
    """
    Test that the model raises a ValidationError when metadata field is missing.
    """
    data = {
        "message_id": "CAPY123456789ABCDEFGHIJKLMNOP"
    }

    with pytest.raises(ValidationError) as excinfo:
        UpdateMessageMetadataRequest(**data)

    error_message = str(excinfo.value)

    assert "Field required" in error_message or "field required" in error_message
    assert "metadata" in error_message
