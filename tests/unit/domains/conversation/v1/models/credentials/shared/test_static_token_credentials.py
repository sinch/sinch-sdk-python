import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.static_token_credentials import (
    StaticTokenCredentials,
)


def test_static_token_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StaticTokenCredentials(token="my-static-token")

    assert model.token == "my-static-token"


def test_static_token_credentials_expects_validation_error_for_missing_token():
    """Test that a ValidationError is raised when the required token is missing."""
    with pytest.raises(ValidationError) as excinfo:
        StaticTokenCredentials()

    assert "token" in str(excinfo.value)
