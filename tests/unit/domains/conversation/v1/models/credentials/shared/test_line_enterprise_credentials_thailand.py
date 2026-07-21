import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials_thailand import (
    LineEnterpriseCredentialsThailand,
)
from sinch.domains.conversation.models.v1.credentials.shared.line_enterprise_credentials import (
    LineEnterpriseCredentials,
)


def test_line_enterprise_credentials_thailand_expects_parsed_input():
    """Test that the model correctly parses a full valid input, including nested credentials."""
    model = LineEnterpriseCredentialsThailand(
        line_thailand={"token": "th-token", "secret": "th-secret"},
        is_default=False,
    )

    assert isinstance(model.line_thailand, LineEnterpriseCredentials)
    assert model.line_thailand.token == "th-token"
    assert model.line_thailand.secret == "th-secret"
    assert model.is_default is False


def test_line_enterprise_credentials_thailand_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = LineEnterpriseCredentialsThailand(line_thailand={"token": "th-token", "secret": "th-secret"},)

    assert model.is_default is None
