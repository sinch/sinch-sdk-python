import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.exceptions import SmsException
from datetime import datetime, timezone

from sinch.domains.sms.api.v1.internal.groups_endpoints import ListGroupsEndpoint
from sinch.domains.sms.models.v1.internal.list_groups_request import ListGroupsRequest
from sinch.domains.sms.models.v1.response.list_groups_response import ListGroupsResponse


@pytest.fixture
def request_data():
    return ListGroupsRequest(page=1, page_size=10)


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "count": 1,
            "page": 0,
            "page_size": 10,
            "groups": [{
                "id": "01FC66621XXXXX119Z8PMV1QPQ",
                "name": "Test Group",
                "size": 2,
                "created_at": "2024-06-06T09:22:14.304Z",
                "modified_at": "2024-06-06T09:22:48.054Z",
                "child_groups": ["01FC66621VHDBN119Z8PMV1AHY"],
                "auto_update": {
                    "to": "+15551231234",
                    "add": {"first_word": "JOIN"},
                    "remove": {"first_word": "LEAVE"},
                },
            }],
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=400,
        body={
            "code": 400,
            "text": "Bad Request",
            "status": "BadRequest",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return ListGroupsEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_sms):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/groups"
    )


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, ListGroupsResponse)
    assert parsed_response.count == 1
    assert parsed_response.page == 0
    assert parsed_response.page_size == 10
    assert len(parsed_response.groups) == 1
    group = parsed_response.groups[0]
    assert group.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert group.name == "Test Group"
    assert group.size == 2
    assert group.child_groups == ["01FC66621VHDBN119Z8PMV1AHY"]
    assert group.auto_update.to == "+15551231234"
    assert group.auto_update.add.first_word == "JOIN"
    assert group.auto_update.remove.first_word == "LEAVE"

    assert group.created_at == datetime(
        2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc
    )
    assert group.modified_at == datetime(
        2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc
    )


def test_handle_response_expects_sms_exception_on_error(
    endpoint, mock_error_response
):
    """
    Test that SmsException is raised when server returns an error.
    """
    with pytest.raises(SmsException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400


def test_build_query_params(endpoint):
    """Test that query params are built correctly from request data."""
    params = endpoint.build_query_params()
    assert params == {"page": 1, "page_size": 10}

