import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.telegram_credentials import (
    TelegramCredentials,
)


def test_telegram_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = TelegramCredentials(token="bot-token")

    assert model.token == "bot-token"


def test_telegram_credentials_expects_validation_error_for_missing_token():
    """Test that a ValidationError is raised when the required token is missing."""
    with pytest.raises(ValidationError) as excinfo:
        TelegramCredentials()

    assert "token" in str(excinfo.value)
