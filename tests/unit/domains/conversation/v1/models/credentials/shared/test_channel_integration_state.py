import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.credentials.shared.channel_integration_state import (
    ChannelIntegrationState,
)


@pytest.mark.parametrize("status", ["PENDING", "ACTIVE", "FAILING"])
def test_channel_integration_state_expects_parsed_input(status):
    """Test that the model correctly parses a full valid input."""
    model = ChannelIntegrationState(
        status=status,
        description="integration description",
    )

    assert model.status == status
    assert model.description == "integration description"


def test_channel_integration_state_expects_description_defaults_to_none():
    """Test that the optional description defaults to None."""
    model = ChannelIntegrationState(status="ACTIVE")

    assert model.description is None


def test_channel_integration_state_expects_validation_error_for_missing_status():
    """Test that a ValidationError is raised when the required status is missing."""
    with pytest.raises(ValidationError) as excinfo:
        ChannelIntegrationState(description="no status")

    assert "status" in str(excinfo.value)
