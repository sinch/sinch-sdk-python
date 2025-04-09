from datetime import datetime, timezone
import pytest
from sinch.domains.numbers.webhooks.v1 import NumbersWebhooks
from sinch.domains.numbers.webhooks.v1.events import NumbersWebhooksEvent


@pytest.fixture
def string_to_sign():
    return (
        '{"eventId":"01jr7stexp0znky34pj07dwp41","timestamp":"2025-04-07T09:38:04.85408760",'
        '"projectId":"project-id","resourceId":"+1234567890",'
        '"resourceType":"ACTIVE_NUMBER","eventType":"PROVISIONING_TO_VOICE_PLATFORM",'
        '"status":"SUCCEEDED","failureCode":null,"internalFailureCode":null}'
    )


@pytest.fixture
def numbers_webhooks():
    return NumbersWebhooks('my-callback-secret')


@pytest.fixture
def base_payload_parse_event():
    return {
        "eventId": "01jr7stexp0znky34pj07dwp41",
        "projectId": "project-id",
        "resourceId": "+1234567890",
        "resourceType": "ACTIVE_NUMBER",
        "eventType": "PROVISIONING_TO_VOICE_PLATFORM",
        "status": "SUCCEEDED",
        "failureCode": None,
        "internalFailureCode": None,
        "timestamp": "2025-04-07T09:38:04.854087603"
    }


def test_valid_signature_header_expects_successful_validation(numbers_webhooks, string_to_sign):
    headers = {
        "X-Sinch-Signature": "8e58baa351ffa5e0d7eaef3c739d0d7aa6093da3"
    }
    response = numbers_webhooks.validate_authentication_header(headers, string_to_sign)
    assert response is True


@pytest.mark.parametrize(
    "test_name, timestamp_str",
    [
        (
            "parse_without_timezone_suffix", "2025-04-06T08:45:27.565347"
        ),
        (
            "parse_with_zulu_timezone_suffix", "2025-04-06T08:45:27.565347Z"
        ),
        (
            "parse_with_extra_digits", "2025-04-06T08:45:27.56534760"
        )
    ]
)
def test_parse_event_expects_timestamp_as_utc(numbers_webhooks, test_name, timestamp_str):
    payload = {"timestamp": timestamp_str}
    parsed = numbers_webhooks.parse_event(payload)
    expected = datetime(
        2025, 4, 6, 8, 45, 27, 565347, tzinfo=timezone.utc
    )
    assert parsed.timestamp == expected


def test_parse_event_expects_parsed_response(numbers_webhooks, base_payload_parse_event):
    response = numbers_webhooks.parse_event(base_payload_parse_event)
    assert isinstance(response, NumbersWebhooksEvent)
    assert response.event_id == "01jr7stexp0znky34pj07dwp41"
    assert response.project_id == "project-id"
    assert response.resource_id == "+1234567890"
    assert response.resource_type == "ACTIVE_NUMBER"
    assert response.event_type == "PROVISIONING_TO_VOICE_PLATFORM"
    assert response.status == "SUCCEEDED"
    assert response.failure_code is None
    assert response.internal_failure_code is None
    expected_timestamp = datetime(
        2025, 4, 7, 9, 38, 4, 854087, tzinfo=timezone.utc
    )
    assert response.timestamp == expected_timestamp
