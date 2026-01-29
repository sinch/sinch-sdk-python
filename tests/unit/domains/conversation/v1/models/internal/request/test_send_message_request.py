import pytest
from pydantic import ValidationError
from sinch.domains.conversation.models.v1.messages.categories.text import TextMessage
from sinch.domains.conversation.models.v1.messages.internal.request import (
    Recipient,
    SendMessageRequestBody,
    SendMessageRequest,
)


def test_send_message_request_expects_parsed_input():
    """
    Test that the model parses input correctly.
    """
    request = SendMessageRequest(
        app_id="my-app-id",
        recipient=Recipient(contact_id="my-contact-id"),
        message=SendMessageRequestBody(text_message=TextMessage(text="Hello")),
    )

    assert request.app_id == "my-app-id"
    assert request.recipient.contact_id == "my-contact-id"
    assert request.message.text_message is not None
    assert request.message.text_message.text == "Hello"


@pytest.mark.parametrize("processing_strategy", ["DEFAULT", "DISPATCH_ONLY"])
def test_send_message_request_expects_accepts_processing_strategy(processing_strategy):
    """
    Test that the model accepts processing_strategy with different values.
    """
    request = SendMessageRequest(
        app_id="my-app-id",
        recipient=Recipient(contact_id="my-contact-id"),
        message=SendMessageRequestBody(text_message=TextMessage(text="Hello")),
        processing_strategy=processing_strategy,
    )

    assert request.processing_strategy == processing_strategy


@pytest.mark.parametrize("ttl_input,expected_serialized", [(10, "10s"), ("10s", "10s"), ("10", "10s"), (None, None)])
def test_send_message_request_expects_ttl_serialized_to_backend(ttl_input, expected_serialized):
    """
    Test that ttl is serialized as "10s" when sent to the backend (int/str normalized to string with 's' suffix).
    """
    request = SendMessageRequest(
        app_id="my-app-id",
        recipient=Recipient(contact_id="my-contact-id"),
        message=SendMessageRequestBody(text_message=TextMessage(text="Hello")),
        ttl=ttl_input,
    )

    payload = request.model_dump(mode="json", exclude_none=True)
    if expected_serialized is None:
        assert "ttl" not in payload
    else:
        assert payload["ttl"] == expected_serialized


def test_send_message_request_expects_validation_error_for_missing_app_id():
    """
    Test that the model raises a ValidationError when app_id field is missing.
    """
    data = {
        "recipient": Recipient(contact_id="my-contact-id"),
        "message": SendMessageRequestBody(text_message=TextMessage(text="Hello")),
    }

    with pytest.raises(ValidationError) as excinfo:
        SendMessageRequest(**data)

    error_message = str(excinfo.value)

    assert "Field required" in error_message or "field required" in error_message
    assert "app_id" in error_message


def test_send_message_request_expects_validation_error_for_missing_recipient():
    """
    Test that the model raises a ValidationError when recipient field is missing.
    """
    data = {
        "app_id": "my-app-id",
        "message": SendMessageRequestBody(text_message=TextMessage(text="Hello")),
    }

    with pytest.raises(ValidationError) as excinfo:
        SendMessageRequest(**data)

    error_message = str(excinfo.value)

    assert "Field required" in error_message or "field required" in error_message
    assert "recipient" in error_message
