import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.event_destinations.request.update_event_destination_request import (
    UpdateEventDestinationRequest,
)
from sinch.domains.conversation.models.v1.event_destinations.shared.client_credentials import (
    ClientCredentials,
)


def test_update_event_destination_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = UpdateEventDestinationRequest(
        event_destination_id="01W4FFL35P4NC4K35WEBHOOK001",
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        target="https://my-server.com/events",
        target_type="HTTP",
        secret="my-secret",
        triggers=["CAPABILITY"],
        client_credentials={
            "endpoint": "https://my-auth-server.com/oauth2/token",
            "client_id": "my-client-id",
            "client_secret": "my-client-secret",
        },
    )

    assert model.event_destination_id == "01W4FFL35P4NC4K35WEBHOOK001"
    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.target == "https://my-server.com/events"
    assert model.target_type == "HTTP"
    assert model.secret == "my-secret"
    assert model.triggers == ["CAPABILITY"]
    assert isinstance(model.client_credentials, ClientCredentials)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["event_destination_id"] == "01W4FFL35P4NC4K35WEBHOOK001"
    assert alias_dump["target_type"] == "HTTP"


def test_update_event_destination_request_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = UpdateEventDestinationRequest(
        event_destination_id="01W4FFL35P4NC4K35WEBHOOK001"
    )

    assert model.app_id is None
    assert model.client_credentials is None
    assert model.secret is None
    assert model.target is None
    assert model.target_type is None
    assert model.triggers is None


def test_update_event_destination_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        UpdateEventDestinationRequest(target="https://my-server.com/events")
