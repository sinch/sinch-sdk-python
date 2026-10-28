"""
Unit tests for Conversation Consents API
"""

import pytest

from sinch.core.pagination import TokenBasedPaginator
from sinch.domains.conversation.api.v1 import Consents
from sinch.domains.conversation.api.v1.internal.consents_endpoints import (
    ListAuditRecordsEndpoint,
    ListConsentIdentitiesEndpoint,
)
from sinch.domains.conversation.conversation import Conversation
from sinch.domains.conversation.models.v1.consents.internal.list_audit_records_request import (
    ListAuditRecordsRequest,
)
from sinch.domains.conversation.models.v1.consents.internal.list_consent_identities_request import (
    ListConsentIdentitiesRequest,
)
from sinch.domains.conversation.models.v1.consents.internal.list_consent_identities_response import (
    ListConsentIdentitiesResponse,
)
from sinch.domains.conversation.models.v1.consents.response.audit_records_response import (
    AuditRecordsResponse,
)

APP_ID = "01W4FFL35P4NC4K35CONVAPP001"
IDENTITY = "33612345678"


def test_conversation_expects_consents_attribute(
    mock_sinch_client_conversation,
):
    """Test that Conversation exposes .consents as a Consents instance."""
    conversation = Conversation(mock_sinch_client_conversation)

    assert isinstance(conversation.consents, Consents)


def test_consents_list_identities_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that list_identities builds the request model and returns a TokenBasedPaginator."""
    mock_response = ListConsentIdentitiesResponse(identities=[])
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(ListConsentIdentitiesEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).consents.list_identities(
        app_id=APP_ID,
        list_type="OPT_OUT_MARKETING",
        page_size=5,
        page_token="token_abc",
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, ListConsentIdentitiesRequest)
    assert request_data.app_id == APP_ID
    assert request_data.list_type == "OPT_OUT_MARKETING"
    assert request_data.page_size == 5
    assert request_data.page_token == "token_abc"
    assert isinstance(response, TokenBasedPaginator)
    assert response.result == mock_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()


def test_consents_list_audit_records_expects_correct_request(
    mock_sinch_client_conversation, mocker
):
    """Test that list_audit_records builds the request model and returns the response."""
    mock_response = AuditRecordsResponse(audit_records=[])
    mock_sinch_client_conversation.configuration.transport.request.return_value = mock_response
    spy_endpoint = mocker.spy(ListAuditRecordsEndpoint, "__init__")

    response = Conversation(
        mock_sinch_client_conversation
    ).consents.list_audit_records(app_id=APP_ID, identity=IDENTITY)

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args
    assert kwargs["project_id"] == "test_project_id"
    request_data = kwargs["request_data"]
    assert isinstance(request_data, ListAuditRecordsRequest)
    assert request_data.app_id == APP_ID
    assert request_data.identity == IDENTITY
    assert response == mock_response
    mock_sinch_client_conversation.configuration.transport.request.assert_called_once()
