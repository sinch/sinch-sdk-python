import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.basic_auth_credentials import (
    BasicAuthCredentials,
)


def test_basic_auth_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = BasicAuthCredentials(username="user", password="pass")

    assert model.username == "user"
    assert model.password == "pass"


@pytest.mark.parametrize("missing", ["username", "password"])
def test_basic_auth_credentials_expects_validation_error_for_missing_field(missing):
    """Test that a ValidationError is raised when a required field is missing."""
    data = {"username": "user", "password": "pass"}
    del data[missing]

    with pytest.raises(ValidationError) as excinfo:
        BasicAuthCredentials(**data)

    assert missing in str(excinfo.value)
