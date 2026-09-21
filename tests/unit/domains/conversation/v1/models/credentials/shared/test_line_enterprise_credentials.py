import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials import (
    LineEnterpriseCredentials,
)


def test_line_enterprise_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = LineEnterpriseCredentials(token="line-token", secret="line-secret")

    assert model.token == "line-token"
    assert model.secret == "line-secret"


@pytest.mark.parametrize("missing", ["token", "secret"])
def test_line_enterprise_credentials_expects_validation_error_for_missing_field(missing):
    """Test that a ValidationError is raised when a required field is missing."""
    data = {"token": "line-token", "secret": "line-secret"}
    del data[missing]

    with pytest.raises(ValidationError) as excinfo:
        LineEnterpriseCredentials(**data)

    assert missing in str(excinfo.value)
