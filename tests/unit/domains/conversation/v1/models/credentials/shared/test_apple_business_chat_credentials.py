import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.apple_business_chat_credentials import (
    AppleBusinessChatCredentials,
)


def test_apple_business_chat_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = AppleBusinessChatCredentials(
        business_chat_account_id="bca-id",
        merchant_id="merchant-id",
        apple_pay_certificate_reference="cert-ref",
        apple_pay_certificate_password="cert-pass",
    )

    assert model.business_chat_account_id == "bca-id"
    assert model.merchant_id == "merchant-id"
    assert model.apple_pay_certificate_reference == "cert-ref"
    assert model.apple_pay_certificate_password == "cert-pass"


def test_apple_business_chat_credentials_expects_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = AppleBusinessChatCredentials(business_chat_account_id="bca-id")

    assert model.merchant_id is None
    assert model.apple_pay_certificate_reference is None
    assert model.apple_pay_certificate_password is None


def test_apple_business_chat_credentials_expects_validation_error_for_missing_field():
    """Test that a ValidationError is raised when the required field is missing."""
    with pytest.raises(ValidationError) as excinfo:
        AppleBusinessChatCredentials(merchant_id="merchant-id")

    assert "business_chat_account_id" in str(excinfo.value)
