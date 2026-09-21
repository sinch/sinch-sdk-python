import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.line_credentials import (
    LineCredentials,
)


def test_line_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = LineCredentials(
        token="line-token",
        secret="line-secret",
        is_default=True,
    )

    assert model.token == "line-token"
    assert model.secret == "line-secret"
    assert model.is_default is True


def test_line_credentials_expects_is_default_defaults_to_none():
    """Test that the optional is_default defaults to None."""
    model = LineCredentials(token="line-token", secret="line-secret")

    assert model.is_default is None


@pytest.mark.parametrize("missing", ["token", "secret"])
def test_line_credentials_expects_validation_error_for_missing_field(missing):
    """Test that a ValidationError is raised when a required field is missing."""
    data = {"token": "line-token", "secret": "line-secret"}
    del data[missing]

    with pytest.raises(ValidationError) as excinfo:
        LineCredentials(**data)

    assert missing in str(excinfo.value)