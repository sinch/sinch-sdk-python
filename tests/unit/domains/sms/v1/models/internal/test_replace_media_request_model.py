import pytest
from pydantic import ValidationError
from datetime import datetime, timezone
from sinch.domains.sms.models.v1.internal.replace_batch_request import (
    ReplaceMediaRequest,
)
from sinch.domains.sms.models.v1.shared import MediaBody


@pytest.fixture
def sample_replace_media_request_data():
    return {
        "batch_id": "01W4FFL35P4NC4K35SMSBATCH2",
        "to": ["+46876543210", "+46987654321"],
        "from_": "+46800123456",
        "body": MediaBody(
            url="https://capybara.com/video.mp4",
            message="Watch this amazing capybara video!",
            subject="Capybara Video",
        ),
    }


def test_replace_media_request_expects_valid_inputs_and_all_fields(
    sample_replace_media_request_data,
):
    """Test ReplaceMediaRequest with valid inputs and all optional fields."""
    request = ReplaceMediaRequest(**sample_replace_media_request_data)
    assert request.batch_id == sample_replace_media_request_data["batch_id"]
    assert request.to == sample_replace_media_request_data["to"]
    assert request.from_ == sample_replace_media_request_data["from_"]
    assert isinstance(request.body, MediaBody)
    assert request.body.url == "https://capybara.com/video.mp4"
    assert request.body.message == "Watch this amazing capybara video!"
    assert request.body.subject == "Capybara Video"
    assert request.type == "mt_media"
    assert request.delivery_report is None
    assert request.feedback_enabled is None
    assert request.strict_validation is None

    send_at = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    expire_at = datetime(2025, 1, 2, 12, 0, 0, tzinfo=timezone.utc)

    request = ReplaceMediaRequest(
        **sample_replace_media_request_data,
        delivery_report="full",
        send_at=send_at,
        expire_at=expire_at,
        callback_url="https://capybara.com/webhook",
        client_reference="capybara-media-batch-123",
        feedback_enabled=True,
        strict_validation=True,
        parameters={
            "name": {"+46876543210": "Alice", "default": "user"},
            "promo": {"+46876543210": "SUMMER2024"},
        },
    )

    assert request.delivery_report == "full"
    assert request.send_at == send_at
    assert request.expire_at == expire_at
    assert request.callback_url == "https://capybara.com/webhook"
    assert request.client_reference == "capybara-media-batch-123"
    assert request.feedback_enabled is True
    assert request.strict_validation is True
    assert request.parameters["name"]["+46876543210"] == "Alice"
    assert request.parameters["promo"]["+46876543210"] == "SUMMER2024"


@pytest.mark.parametrize(
    "missing_field",
    ["batch_id", "to", "body"],
)
def test_replace_media_request_expects_required_fields(
    sample_replace_media_request_data, missing_field
):
    """Test that ReplaceMediaRequest requires batch_id, to, and body fields."""
    data = sample_replace_media_request_data.copy()
    data.pop(missing_field)
    with pytest.raises(ValidationError) as exc_info:
        ReplaceMediaRequest(**data)
    assert missing_field in str(exc_info.value)


def test_replace_media_request_expects_body_must_be_media_body(
    sample_replace_media_request_data,
):
    """Test that body must be a MediaBody instance or dict that can be converted."""
    data = sample_replace_media_request_data.copy()
    data["body"] = "invalid"
    with pytest.raises(ValidationError):
        ReplaceMediaRequest(**data)

    data["body"] = None
    with pytest.raises(ValidationError):
        ReplaceMediaRequest(**data)

    data["body"] = {"url": "https://capybara.com/audio.mp3"}
    request = ReplaceMediaRequest(**data)
    assert isinstance(request.body, MediaBody)
    assert request.body.url == "https://capybara.com/audio.mp3"
