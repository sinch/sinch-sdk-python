import pytest
from pydantic import ValidationError
from sinch.domains.conversation.models.v1.messages.internal.request import (
    MessageIdRequest,
)


def test_message_id_request_expects_accepts_snake_case_input():
    """
    Test that the model accepts snake_case input when allow_population_by_field_name is True.
    """
    request = MessageIdRequest(message_id="CAPYLAKE123456789ABCDEFGHIJKL")

    assert request.message_id == "CAPYLAKE123456789ABCDEFGHIJKL"


@pytest.mark.parametrize("messages_source", ["CONVERSATION_SOURCE", "DISPATCH_SOURCE"])
def test_message_id_request_expects_accepts_messages_source(messages_source):
    """
    Test that the model accepts messages_source with different values.
    """
    request = MessageIdRequest(
        message_id="CAPYPOUND123456789ABCDEFGHIJKLM",
        messages_source=messages_source
    )

    assert request.message_id == "CAPYPOUND123456789ABCDEFGHIJKLM"
    assert request.messages_source == messages_source


def test_message_id_request_expects_validation_error_for_missing_field():
    """
    Test that the model raises a ValidationError when a required field is missing.
    """
    data = {}

    with pytest.raises(ValidationError) as excinfo:
        MessageIdRequest(**data)

    error_message = str(excinfo.value)

    assert "Field required" in error_message or "field required" in error_message
    assert "messageId" in error_message or "message_id" in error_message
