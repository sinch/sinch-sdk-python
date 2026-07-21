import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.instagram_credentials import (
    InstagramCredentials,
)


def test_instagram_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = InstagramCredentials(
        token="ig-token",
        business_account_id="123456",
    )

    assert model.token == "ig-token"
    assert model.business_account_id == "123456"


def test_instagram_credentials_expects_business_account_id_defaults_to_none():
    """Test that the optional business_account_id defaults to None."""
    model = InstagramCredentials(token="ig-token")

    assert model.business_account_id is None


def test_instagram_credentials_expects_validation_error_for_missing_token():
    """Test that a ValidationError is raised when the required token is missing."""
    with pytest.raises(ValidationError) as excinfo:
        InstagramCredentials(business_account_id="123456")

    assert "token" in str(excinfo.value)
