import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.mms_credentials import (
    MMSCredentials,
)
from sinch.domains.conversation.models.v1.credentials.shared.basic_auth_credentials import (
    BasicAuthCredentials,
)


def test_mms_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input, including nested basic_auth."""
    model = MMSCredentials(
        account_id="acc-id",
        api_key="api-key",
        basic_auth={"username": "user", "password": "pass"},
    )

    assert model.account_id == "acc-id"
    assert model.api_key == "api-key"
    assert isinstance(model.basic_auth, BasicAuthCredentials)
    assert model.basic_auth.username == "user"
    assert model.basic_auth.password == "pass"


def test_mms_credentials_expects_basic_auth_defaults_to_none():
    """Test that the optional basic_auth defaults to None."""
    model = MMSCredentials(account_id="acc-id", api_key="api-key")

    assert model.basic_auth is None


@pytest.mark.parametrize("missing", ["account_id", "api_key"])
def test_mms_credentials_expects_validation_error_for_missing_field(missing):
    """Test that a ValidationError is raised when a required field is missing."""
    data = {"account_id": "acc-id", "api_key": "api-key"}
    del data[missing]

    with pytest.raises(ValidationError) as excinfo:
        MMSCredentials(**data)

    assert missing in str(excinfo.value)
