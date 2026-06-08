from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from sinch.domains.sms.models.v1.shared import MOMediaBody, MOMediaItem, MOMediaMessage


@pytest.fixture
def sample_mo_media_data():
    return {
        "from": "+46701234567",
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": "+46709876543",
        "type": "mo_media",
        "received_at": "2024-06-06T09:22:14.304Z",
        "body": {
            "subject": "MMS subject",
            "message": "Hello media",
            "media": [
                {
                    "url": "https://example.com/img.jpg",
                    "content_type": "image/jpeg",
                    "status": "Uploaded",
                    "code": 200,
                }
            ],
        },
    }


def test_mo_media_message_expects_valid_input(sample_mo_media_data):
    """Test that the model correctly parses valid input including nested body."""
    msg = MOMediaMessage(**sample_mo_media_data)

    assert msg.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert msg.from_ == "+46701234567"
    assert msg.to == "+46709876543"
    assert msg.type == "mo_media"
    assert msg.received_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)

    assert isinstance(msg.body, MOMediaBody)
    assert msg.body.subject == "MMS subject"
    assert msg.body.message == "Hello media"
    assert msg.body.media is not None
    assert len(msg.body.media) == 1

    item = msg.body.media[0]
    assert isinstance(item, MOMediaItem)
    assert item.url == "https://example.com/img.jpg"
    assert item.content_type == "image/jpeg"
    assert item.status == "Uploaded"
    assert item.code == 200


def test_mo_media_message_expects_body_with_no_media():
    """Test that body with no media attachment is valid."""
    data = {
        "from": "+46701234567",
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": "+46709876543",
        "type": "mo_media",
        "received_at": "2024-06-06T09:22:14.304Z",
        "body": {
            "subject": "Hi",
            "message": "Text only MMS",
        },
    }
    msg = MOMediaMessage(**data)

    assert msg.body.subject == "Hi"
    assert msg.body.message == "Text only MMS"
    assert msg.body.media is None


def test_mo_media_message_expects_optional_fields_none(sample_mo_media_data):
    """Test that optional base fields default to None."""
    msg = MOMediaMessage(**sample_mo_media_data)

    assert msg.client_reference is None
    assert msg.operator_id is None
    assert msg.sent_at is None


def test_mo_media_message_expects_validation_error_for_missing_body():
    """Test that missing required body field raises a ValidationError."""
    data = {
        "from": "+46701234567",
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": "+46709876543",
        "type": "mo_media",
        "received_at": "2024-06-06T09:22:14.304Z",
    }
    with pytest.raises(ValidationError) as exc_info:
        MOMediaMessage(**data)

    assert "body" in str(exc_info.value)
