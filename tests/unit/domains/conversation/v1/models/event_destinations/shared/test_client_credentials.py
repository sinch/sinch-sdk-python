import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.event_destinations.shared.client_credentials import (
    ClientCredentials,
)


def test_client_credentials_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ClientCredentials(
        client_id="my-client-id",
        client_secret="my-client-secret",
        endpoint="https://my-auth-server.com/oauth2/token",
        scope="read write",
        response_type="token",
        token_request_type="FORM",
    )

    assert model.client_id == "my-client-id"
    assert model.client_secret == "my-client-secret"
    assert model.endpoint == "https://my-auth-server.com/oauth2/token"
    assert model.scope == "read write"
    assert model.response_type == "token"
    assert model.token_request_type == "FORM"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["client_id"] == "my-client-id"
    assert alias_dump["token_request_type"] == "FORM"


def test_client_credentials_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = ClientCredentials(
        client_id="my-client-id",
        client_secret="my-client-secret",
        endpoint="https://my-auth-server.com/oauth2/token",
    )

    assert model.scope is None
    assert model.response_type is None
    assert model.token_request_type is None


def test_client_credentials_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        ClientCredentials(
            client_id="my-client-id",
            client_secret="my-client-secret",
        )
