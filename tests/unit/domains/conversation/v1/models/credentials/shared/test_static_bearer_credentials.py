import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.static_bearer_credentials import (
    StaticBearerCredentials,
)


def test_static_bearer_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StaticBearerCredentials(
        claimed_identity="my-identity",
        token="my-bearer-token",
    )

    assert model.claimed_identity == "my-identity"
    assert model.token == "my-bearer-token"


@pytest.mark.parametrize("missing", ["claimed_identity", "token"])
def test_static_bearer_credentials_expects_validation_error_for_missing_field(missing):
    """Test that a ValidationError is raised when a required field is missing."""
    data = {"claimed_identity": "my-identity", "token": "my-bearer-token"}
    del data[missing]

    with pytest.raises(ValidationError) as excinfo:
        StaticBearerCredentials(**data)

    assert missing in str(excinfo.value)

