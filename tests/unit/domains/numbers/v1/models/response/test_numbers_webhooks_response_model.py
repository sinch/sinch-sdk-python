import pytest
from datetime import datetime, timezone
from pydantic import ValidationError
from sinch.domains.numbers.models.v1.response import NumbersWebhooksResponse


@pytest.fixture
def valid_data():
    return {
        "eventId": "event-123",
        "timestamp": "2025-04-08T09:38:04.854087+00:00",
        "projectId": "project-456",
        "resourceId": "+1234567890",
        "resourceType": "ACTIVE_NUMBER",
        "eventType": "PROVISIONING_TO_VOICE_PLATFORM",
        "status": "SUCCEEDED",
        "failureCode": None,
        "internalFailureCode": None,
        "extraField": "extra_value"
    }


@pytest.fixture
def invalid_data():
    return {
        "eventId": 123,
        "timestamp": "invalid-timestamp",
        "projectId": "project-456",
        "resourceId": "+1234567890"
    }


def test_numbers_webhooks_response_expects_parsed_data(valid_data):
    """
    Expects all fields to map correctly from camelCase input
    and handle valid data appropriately.
    """
    response = NumbersWebhooksResponse(**valid_data)

    assert response.event_id == "event-123"
    assert response.timestamp == datetime(
        2025, 4, 8, 9, 38, 4, 854087, tzinfo=timezone.utc
    )
    assert response.project_id == "project-456"
    assert response.resource_id == "+1234567890"
    assert response.resource_type == "ACTIVE_NUMBER"
    assert response.event_type == "PROVISIONING_TO_VOICE_PLATFORM"
    assert response.status == "SUCCEEDED"
    assert response.failure_code is None
    assert response.internal_failure_code is None
    assert response.extra_field == "extra_value"


def test_numbers_webhooks_response_missing_optional_fields_expects_parsed_data():
    """
    Expects the model to handle missing optional fields.
    """
    data = {
        "eventId": "event-123",
        "projectId": "project-456"
    }
    response = NumbersWebhooksResponse(**data)

    assert response.event_id == "event-123"
    assert response.project_id == "project-456"
    assert response.timestamp is None
    assert response.resource_id is None
    assert response.resource_type is None
    assert response.event_type is None
    assert response.status is None
    assert response.failure_code is None


def test_numbers_webhooks_response_invalid_data_expects_validation_error(invalid_data):
    """
    Expects the model to raise a validation error for invalid data.
    """
    with pytest.raises(ValidationError):
        NumbersWebhooksResponse(**invalid_data)
