from datetime import datetime, timezone
import pytest
from pydantic import ValidationError, TypeAdapter
from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.sms.models.v1.types import BatchResponse
from sinch.domains.sms.models.v1.shared.text_response import TextResponse
from sinch.domains.sms.models.v1.shared.binary_response import BinaryResponse
from sinch.domains.sms.models.v1.shared.media_response import MediaResponse


@pytest.fixture
def text_response_data():
    """Sample TextResponse data for testing."""
    return {
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": ["12017777777"],
        "from": "12015555555",
        "canceled": False,
        "body": "Hello World!",
        "type": "mt_text",
        "created_at": "2024-01-15T14:30:22.123Z",
        "modified_at": "2024-01-15T14:35:45.789Z",
        "delivery_report": "full",
        "send_at": "2024-01-15T15:00:00Z",
        "expire_at": "2024-01-18T15:00:00Z",
        "feedback_enabled": True,
        "flash_message": False,
    }


@pytest.fixture
def binary_response_data():
    """Sample BinaryResponse data for testing."""
    return {
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": ["12017777777"],
        "from": "12015555555",
        "canceled": False,
        "body": "SGVsbG8gV29ybGQh",
        "udh": "06050423F423F4",
        "type": "mt_binary",
        "created_at": "2024-03-20T08:15:33.456Z",
        "modified_at": "2024-03-20T08:16:12.890Z",
    }


@pytest.fixture
def media_response_data():
    """Sample MediaResponse data for testing."""
    return {
        "id": "01FC66621XXXXX119Z8PMV1QPQ",
        "to": ["12017777777"],
        "from": "12015555555",
        "canceled": False,
        "body": {
            "url": "https://example.com/image.jpg",
            "message": "Check out this image!",
        },
        "type": "mt_media",
        "created_at": "2024-11-10T16:45:10.234Z",
        "modified_at": "2024-11-10T16:47:22.567Z",
    }


@pytest.mark.parametrize(
    "payload_fixture, expected_type, expected_fields",
    [
        (
            "text_response_data",
            TextResponse,
            {"body": "Hello World!", "delivery_report": "full"},
        ),
        ("binary_response_data", BinaryResponse, {"udh": "06050423F423F4"}),
        ("media_response_data", MediaResponse, {}),
    ],
    ids=["text", "binary", "media"],
)
def test_batch_response_expects_each_variant_resolved(
    request, payload_fixture, expected_type, expected_fields
):
    """
    Test that each batch response variant is resolved from its type field.
    """
    payload = request.getfixturevalue(payload_fixture)

    with response_parsing_scope():
        response = TypeAdapter(BatchResponse).validate_python(payload)

    assert type(response) is expected_type
    for name, value in expected_fields.items():
        assert getattr(response, name) == value


def test_batch_response_expects_unknown_type_resolved_to_unknown():
    """
    Test that a batch type added to the API later is parsed as SinchRawResponse,
    keeping the payload, instead of failing the whole response.
    """
    payload = {"type": "mt_future", "id": "test123", "body": "Hello"}

    with response_parsing_scope():
        response = TypeAdapter(BatchResponse).validate_python(payload)

    assert isinstance(response, SinchRawResponse)
    assert response.model_dump() == payload


def test_batch_response_expects_text_response_variations(text_response_data):
    """
    Test TextResponse variations: minimal fields, parameters, and datetime parsing.
    """
    adapter = TypeAdapter(BatchResponse)

    minimal_data = {"type": "mt_text", "id": "01FC66621XXXXX119Z8PMV1QPQ"}
    response = adapter.validate_python(minimal_data)
    assert isinstance(response, TextResponse)
    assert response.type == "mt_text"
    assert response.canceled is None

    text_response_data["parameters"] = {
        "name": {"+12017777777": "John", "default": "there"},
        "code": {"+12017777777": "HALLOWEEN20"},
    }
    response = adapter.validate_python(text_response_data)
    assert isinstance(response, TextResponse)
    assert response.parameters["name"]["+12017777777"] == "John"
    assert response.parameters["code"]["+12017777777"] == "HALLOWEEN20"

    expected_created_at = datetime(
        2024, 1, 15, 14, 30, 22, 123000, tzinfo=timezone.utc
    )
    expected_modified_at = datetime(
        2024, 1, 15, 14, 35, 45, 789000, tzinfo=timezone.utc
    )
    expected_send_at = datetime(2024, 1, 15, 15, 0, 0, tzinfo=timezone.utc)
    expected_expire_at = datetime(2024, 1, 18, 15, 0, 0, tzinfo=timezone.utc)
    assert response.created_at == expected_created_at
    assert response.modified_at == expected_modified_at
    assert response.send_at == expected_send_at
    assert response.expire_at == expected_expire_at

    text_response_data["canceled"] = True
    response = adapter.validate_python(text_response_data)
    assert response.canceled is True


def test_batch_response_expects_discriminator_behavior():
    """
    Test discriminator behavior: routing by type field, handling invalid/missing types,
    and working with extra fields.
    """
    adapter = TypeAdapter(BatchResponse)

    # Discriminator routes by type field, not field presence
    data_with_binary_fields_but_text_type = {
        "type": "mt_text",
        "id": "test123",
        "body": "SGVsbG8gV29ybGQh",
        "udh": "06050423F423F4",
    }
    response = adapter.validate_python(data_with_binary_fields_but_text_type)
    assert isinstance(response, TextResponse)
    assert response.type == "mt_text"
    assert hasattr(response, "udh")

    # Invalid type should be rejected
    with pytest.raises(ValidationError):
        adapter.validate_python({"id": "test", "type": "invalid_type"})

    # Missing type field should cause validation error
    with pytest.raises(ValidationError):
        adapter.validate_python({"id": "test", "body": "Hello"})

    # Extra fields are allowed and don't affect routing
    text_with_extra = {
        "type": "mt_text",
        "id": "test",
        "body": "Hello",
        "extra": "value",
    }
    response = adapter.validate_python(text_with_extra)
    assert isinstance(response, TextResponse)

    binary_with_extra = {
        "type": "mt_binary",
        "id": "test",
        "body": "SGVsbG8=",
        "udh": "06050423F4",
        "extra": "value",
    }
    response = adapter.validate_python(binary_with_extra)
    assert isinstance(response, BinaryResponse)
