from datetime import datetime, timezone

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.consents_endpoints import (
    ListAuditRecordsEndpoint,
)
from sinch.domains.conversation.models.v1.consents.internal.list_audit_records_request import (
    ListAuditRecordsRequest,
)
from sinch.domains.conversation.models.v1.consents.shared.audit_record import (
    AuditRecord,
)
from sinch.domains.conversation.models.v1.consents.response.audit_records_response import (
    AuditRecordsResponse,
)


@pytest.fixture
def request_data():
    return ListAuditRecordsRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001", identity="33612345678"
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "identity": {"identity": "33612345678"},
            "audit_records": [
                {
                    "origin": "ORIGIN_MO",
                    "operation": "OPERATION_INSERT",
                    "list_type": "OPT_OUT_ALL",
                    "project_id": "test_project_id",
                    "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                    "datetime": "2025-06-06T14:42:56.031323Z",
                }
            ],
            "unexpected_field": "kept",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=404,
        body={
            "error": {
                "code": 404,
                "message": "information not found",
                "status": "NOT_FOUND",
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return ListAuditRecordsEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL contains the app ID and the identity."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/apps/01W4FFL35P4NC4K35CONVAPP001/consents/identities/33612345678"
    )


def test_build_query_params_expects_no_query_params(endpoint):
    """Test that no query params are sent."""
    assert endpoint.build_query_params() == {}


def test_request_body_expects_no_body(endpoint):
    """Test that a GET request has no body."""
    assert endpoint.request_body() is None


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into an AuditRecordsResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, AuditRecordsResponse)
    assert parsed_response.identity.identity == "33612345678"
    assert len(parsed_response.audit_records) == 1
    record = parsed_response.audit_records[0]
    assert isinstance(record, AuditRecord)
    assert record.origin == "ORIGIN_MO"
    assert record.operation == "OPERATION_INSERT"
    assert record.list_type == "OPT_OUT_ALL"
    assert record.project_id == "test_project_id"
    assert record.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert record.datetime == datetime(
        2025, 6, 6, 14, 42, 56, 31323, tzinfo=timezone.utc
    )
    assert parsed_response.unexpected_field == "kept"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "information not found  NOT_FOUND"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404
