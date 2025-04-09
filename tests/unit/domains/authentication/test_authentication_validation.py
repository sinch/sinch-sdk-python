import pytest
from sinch.domains.authentication.webhooks.v1.authentication_validation import validate_signature_header


@pytest.fixture
def string_to_sign():
    return (
        '{"eventId":"event_id","timestamp":"2025-04-08T10:38:04.854087603",'
        '"projectId":"project-id","resourceId":"+1234567890",'
        '"resourceType":"ACTIVE_NUMBER","eventType":"PROVISIONING_TO_VOICE_PLATFORM",'
        '"status":"SUCCEEDED","failureCode":null,"internalFailureCode":null}'
    )


@pytest.fixture
def secret():
    return "my-callback-secret"


def test_valid_signature_header_expects_successful_validation(secret, string_to_sign):
    headers = {
        "X-Sinch-Signature": "d2107528d5d52897a97dc6e24e09a208036ccd83"
    }
    validated = validate_signature_header(secret, headers, string_to_sign)
    assert validated is True


def test_missing_signature_expects_no_validation(secret, string_to_sign):
    headers = {}
    validated = validate_signature_header(secret, headers, string_to_sign)
    assert validated is False


def test_invalid_signature_expects_no_validation(secret, string_to_sign):
    headers = {
        "X-Sinch-Signature": "invalid-signature"
    }
    validated = validate_signature_header(secret, headers, string_to_sign)
    assert validated is False
