"""
Unit tests for Conversation Capability API
"""

import pytest

from sinch.domains.conversation.api.v1 import Capability
from sinch.domains.conversation.api.v1.internal.capability_endpoints import (
    LookupCapabilityEndpoint,
)
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.models.v1.capability.internal.lookup_capability_request import (
    LookupCapabilityRequest,
)
from sinch.domains.conversation.models.v1.capability.response.lookup_capability_response import (
    LookupCapabilityResponse,
)

APP_ID = "01W4FFL35P4NC4K35CONVAPP001"
CONTACT_ID = "01W4FFL35P4NC4K35CONTACT001"
REQUEST_ID = "01W4FFL35P4NC4K35CAPABILITY"


@pytest.fixture
def mock_lookup_capability_response():
    return LookupCapabilityResponse(
        app_id=APP_ID,
        recipient={"contact_id": CONTACT_ID},
        request_id=REQUEST_ID,
    )


def test_conversation_expects_capability_attribute(
    mock_sinch_client_conversation,
):
    """Test that Conversation exposes .capability as a Capability instance."""
    conversation = Conversation(mock_sinch_client_conversation)

    assert isinstance(conversation.capability, Capability)


def test_capability_lookup_expects_correct_request(
    mock_sinch_client_conversation, mock_lookup_capability_response, mocker
):
    """Test that lookup builds the request model from every parameter and returns the response."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_lookup_capability_response
    spy_endpoint = mocker.spy(LookupCapabilityEndpoint, "__init__")

    response = Conversation(mock_sinch_client_conversation).capability.lookup(
        app_id=APP_ID,
        contact_id=CONTACT_ID,
        request_id=REQUEST_ID,
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, LookupCapabilityRequest)
    assert request_data.app_id == APP_ID
    assert request_data.recipient.contact_id == CONTACT_ID
    assert request_data.request_id == REQUEST_ID
    assert isinstance(response, LookupCapabilityResponse)
    assert response.request_id == REQUEST_ID
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_capability_lookup_expects_channel_identities_recipient(
    mock_sinch_client_conversation, mock_lookup_capability_response, mocker
):
    """Test that recipient_identities are wrapped into the identified_by recipient."""
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_lookup_capability_response
    spy_endpoint = mocker.spy(LookupCapabilityEndpoint, "__init__")

    Conversation(mock_sinch_client_conversation).capability.lookup(
        app_id=APP_ID,
        recipient_identities=[{"channel": "SMS", "identity": "46700000000"}],
    )

    _, kwargs = spy_endpoint.call_args
    request_data = kwargs["request_data"]
    identities = request_data.recipient.identified_by.channel_identities
    assert identities[0].channel == "SMS"
    assert identities[0].identity == "46700000000"
    assert request_data.recipient.contact_id is None
    assert "request_id" not in request_data.model_fields_set


def test_capability_lookup_expects_value_error_without_recipient(
    mock_sinch_client_conversation,
):
    """Test that lookup requires exactly one of contact_id or recipient_identities."""
    with pytest.raises(ValueError):
        Conversation(mock_sinch_client_conversation).capability.lookup(
            app_id=APP_ID
        )
