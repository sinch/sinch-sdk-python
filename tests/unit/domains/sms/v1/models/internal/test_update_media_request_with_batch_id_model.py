import pytest
from datetime import datetime, timezone
from sinch.domains.sms.models.v1.internal.update_batch_message_request import (
    UpdateMediaRequestWithBatchId,
)
from sinch.domains.sms.models.v1.shared import MediaBody


@pytest.fixture
def sample_update_media_request_data():
    return {
        "batch_id": "01FC99954AAAAA442C1SPY4TUQ",
        "body": MediaBody(
            url="https://capybara.com/media/video.mp4",
            message="Updated capybara video message",
            subject="Capybara Video Update",
        ),
    }


def test_update_media_request_expects_valid_inputs_and_all_fields(
    sample_update_media_request_data,
):
    """Test UpdateMediaRequestWithBatchId with valid inputs and all optional fields."""
    request = UpdateMediaRequestWithBatchId(**sample_update_media_request_data)
    assert request.batch_id == sample_update_media_request_data["batch_id"]
    assert request.body.url == sample_update_media_request_data["body"].url
    assert (
        request.body.message
        == sample_update_media_request_data["body"].message
    )
    assert (
        request.body.subject
        == sample_update_media_request_data["body"].subject
    )
    assert request.type == "mt_media"

    send_at = datetime(2025, 6, 5, 18, 0, 0, tzinfo=timezone.utc)
    expire_at = datetime(2025, 6, 8, 18, 0, 0, tzinfo=timezone.utc)

    request = UpdateMediaRequestWithBatchId(
        **sample_update_media_request_data,
        from_="+46701010101",
        to_add=["+46701111111", "+46701222222"],
        to_remove=["+46701333333"],
        delivery_report="none",
        send_at=send_at,
        expire_at=expire_at,
        callback_url="https://capybara.com/media-callback",
        client_reference="media-update-789",
        feedback_enabled=True,
        strict_validation=True,
        parameters={
            "media": {"+46701111111": "video1", "default": "video2"},
        },
    )

    assert request.batch_id == sample_update_media_request_data["batch_id"]
    assert request.from_ == "+46701010101"
    assert request.to_add == ["+46701111111", "+46701222222"]
    assert request.to_remove == ["+46701333333"]
    assert request.delivery_report == "none"
    assert request.send_at == send_at
    assert request.expire_at == expire_at
    assert request.callback_url == "https://capybara.com/media-callback"
    assert request.client_reference == "media-update-789"
    assert request.feedback_enabled is True
    assert request.strict_validation is True
    assert request.parameters == {
        "media": {"+46701111111": "video1", "default": "video2"},
    }


def test_update_media_request_expects_datetime_parsing(
    sample_update_media_request_data,
):
    """Test datetime parsing for send_at and expire_at."""
    send_at_str = "2025-07-15T12:30:15.789Z"
    expire_at_str = "2025-07-18T12:30:15.789Z"

    request = UpdateMediaRequestWithBatchId(
        **sample_update_media_request_data,
        send_at=send_at_str,
        expire_at=expire_at_str,
    )

    assert isinstance(request.send_at, datetime)
    assert isinstance(request.expire_at, datetime)


def test_update_media_request_expects_minimal_input(
    sample_update_media_request_data,
):
    """Test UpdateMediaRequestWithBatchId with only required fields."""
    request = UpdateMediaRequestWithBatchId(
        batch_id=sample_update_media_request_data["batch_id"],
    )
    assert request.batch_id == sample_update_media_request_data["batch_id"]
    assert request.body is None
    assert request.type == "mt_media"
    assert request.feedback_enabled is None
    assert request.strict_validation is None
