import json

import pytest

from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.capability_endpoints import (
    LookupCapabilityEndpoint,
)
from sinch.domains.conversation.models.v1.capability.internal.lookup_capability_request import (
    LookupCapabilityRequest,
)
from sinch.domains.conversation.models.v1.capability.response.lookup_capability_response import (
    LookupCapabilityResponse,
)


@pytest.fixture
def request_data():
    return LookupCapabilityRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        recipient={"contact_id": "01W4FFL35P4NC4K35CONTACT001"},
        request_id="01W4FFL35P4NC4K35CAPABILITY",
    )


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "app_id": "01W4FFL35P4NC4K35CONVAPP001",
            "recipient": {"contact_id": "01W4FFL35P4NC4K35CONTACT001"},
            "request_id": "01W4FFL35P4NC4K35CAPABILITY",
            "unexpected_field": "kept",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=400,
        body={
            "error": {
                "code": 400,
                "message": "Invalid argument",
                "status": "INVALID_ARGUMENT",
            }
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return LookupCapabilityEndpoint("test_project_id", request_data)


def test_build_url_expects_correct_url(
    endpoint, mock_sinch_client_conversation
):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_conversation)
        == "https://us.conversation.api.sinch.com/v1/projects/test_project_id/capability:query"
    )


def test_request_body_expects_correct_serialization(endpoint):
    """Test that every field is serialized with its wire name."""
    body = json.loads(endpoint.request_body())

    assert body["app_id"] == "01W4FFL35P4NC4K35CONVAPP001"
    assert body["recipient"] == {"contact_id": "01W4FFL35P4NC4K35CONTACT001"}
    assert body["request_id"] == "01W4FFL35P4NC4K35CAPABILITY"
    assert "project_id" not in body


def test_request_body_expects_identified_by_recipient():
    """Test that a channel identities recipient is serialized under identified_by."""
    endpoint = LookupCapabilityEndpoint(
        "test_project_id",
        LookupCapabilityRequest(
            app_id="01W4FFL35P4NC4K35CONVAPP001",
            recipient={
                "identified_by": {
                    "channel_identities": [
                        {"channel": "SMS", "identity": "46700000000"}
                    ]
                }
            },
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["recipient"] == {
        "identified_by": {
            "channel_identities": [
                {"channel": "SMS", "identity": "46700000000"}
            ]
        }
    }

def test_request_body_accepts_none_fields_and_exclude_unset_fields():
    """Test that an explicit None is sent as null and unset fields are omitted."""
    endpoint = LookupCapabilityEndpoint(
        "test_project_id",
        LookupCapabilityRequest(
            app_id="01W4FFL35P4NC4K35CONVAPP001",
            request_id=None,
            recipient={"contact_id": "01W4FFL35P4NC4K35CONTACT001"},
        ),
    )
    body = json.loads(endpoint.request_body())

    assert body["request_id"] is None
    assert body["app_id"] == "01W4FFL35P4NC4K35CONVAPP001"

    unset_endpoint = LookupCapabilityEndpoint(
        "test_project_id",
        LookupCapabilityRequest(
            app_id="01W4FFL35P4NC4K35CONVAPP001",
            recipient={"contact_id": "01W4FFL35P4NC4K35CONTACT001"},
        ),
    )
    assert "request_id" not in json.loads(unset_endpoint.request_body())


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Test that the response is mapped into a LookupCapabilityResponse."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, LookupCapabilityResponse)
    assert parsed_response.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert (
        parsed_response.recipient.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    )
    assert parsed_response.request_id == "01W4FFL35P4NC4K35CAPABILITY"
    assert parsed_response.unexpected_field == "kept"


def test_handle_response_expects_conversation_exception_on_error(
    endpoint, mock_error_response
):
    """Test that ConversationException is raised with the server error message."""
    with pytest.raises(ConversationException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert str(exc_info.value) == "Invalid argument  INVALID_ARGUMENT"
    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400
