import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.event_destinations.response.event_destination_response import (
    EventDestinationResponse,
)
from sinch.domains.conversation.models.v1.event_destinations.shared.client_credentials import (
    ClientCredentials,
)


def test_event_destination_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = EventDestinationResponse(
        id="01W4FFL35P4NC4K35WEBHOOK001",
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        target="https://my-server.com/events",
        target_type="HTTP",
        secret="my-secret",
        triggers=["CAPABILITY", "OPT_IN"],
        client_credentials={
            "endpoint": "https://my-auth-server.com/oauth2/token",
            "client_id": "my-client-id",
            "client_secret": "my-client-secret",
        },
    )

    assert model.id == "01W4FFL35P4NC4K35WEBHOOK001"
    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.target == "https://my-server.com/events"
    assert model.target_type == "HTTP"
    assert model.secret == "my-secret"
    assert model.triggers == ["CAPABILITY", "OPT_IN"]
    assert isinstance(model.client_credentials, ClientCredentials)
    assert model.client_credentials.client_id == "my-client-id"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "01W4FFL35P4NC4K35CONVAPP001"
    assert alias_dump["target_type"] == "HTTP"
    assert (
        alias_dump["client_credentials"]["client_secret"] == "my-client-secret"
    )


def test_event_destination_response_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = EventDestinationResponse(target="https://my-server.com/events")

    assert model.id is None
    assert model.app_id is None
    assert model.secret is None
    assert model.target_type is None
    assert model.triggers is None
    assert model.client_credentials is None


def test_event_destination_response_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        EventDestinationResponse(id="01W4FFL35P4NC4K35WEBHOOK001")
