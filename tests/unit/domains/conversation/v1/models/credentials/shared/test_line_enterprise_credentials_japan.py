import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_japan import (
    LineEnterpriseCredentialsJapan,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials import (
    LineEnterpriseCredentials,
)


def test_line_enterprise_credentials_japan_expects_parsed_input():
    """Test that the model correctly parses a full valid input, including nested credentials."""
    model = LineEnterpriseCredentialsJapan(
        line_japan={"token": "jp-token", "secret": "jp-secret"},
        is_default=True,
    )

    assert isinstance(model.line_japan, LineEnterpriseCredentials)
    assert model.line_japan.token == "jp-token"
    assert model.line_japan.secret == "jp-secret"
    assert model.is_default is True


def test_line_enterprise_credentials_japan_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = LineEnterpriseCredentialsJapan(line_japan={"token": "jp-token", "secret": "jp-secret"},)

    assert model.is_default is None
