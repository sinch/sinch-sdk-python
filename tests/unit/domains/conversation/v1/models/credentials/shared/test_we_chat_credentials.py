import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.we_chat_credentials import (
    WeChatCredentials,
)


def test_we_chat_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = WeChatCredentials(
        app_id="app-id",
        app_secret="app-secret",
        token="token",
        aes_key="aes-key",
    )

    assert model.app_id == "app-id"
    assert model.app_secret == "app-secret"
    assert model.token == "token"
    assert model.aes_key == "aes-key"


@pytest.mark.parametrize("missing", ["app_id", "app_secret", "token", "aes_key"])
def test_we_chat_credentials_expects_validation_error_for_missing_field(missing):
    """Test that a ValidationError is raised when a required field is missing."""
    data = {
        "app_id": "app-id",
        "app_secret": "app-secret",
        "token": "token",
        "aes_key": "aes-key",
    }
    del data[missing]

    with pytest.raises(ValidationError) as excinfo:
        WeChatCredentials(**data)

    assert missing in str(excinfo.value)