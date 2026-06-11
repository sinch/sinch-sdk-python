import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.exceptions import SmsException

from sinch.domains.sms.api.v1.internal.groups_endpoints import DeleteGroupEndpoint
from sinch.domains.sms.models.v1.internal.group_id_request import GroupIdRequest


@pytest.fixture
def request_data():
    return GroupIdRequest(group_id="01FC66621XXXXX119Z8PMV1QPQ")


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=204,
        body={},
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def mock_error_response():
    return HTTPResponse(
        status_code=404,
        body={
            "code": 404,
            "text": "Group not found",
            "status": "NotFound",
        },
        headers={"Content-Type": "application/json"},
    )


@pytest.fixture
def endpoint(request_data):
    return DeleteGroupEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_sms):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/groups/01FC66621XXXXX119Z8PMV1QPQ"
    )


def test_handle_response_returns_none(endpoint, mock_response):
    """Test that handle_response returns None for a successful delete."""
    result = endpoint.handle_response(mock_response)
    assert result is None


def test_handle_response_expects_sms_exception_on_error(endpoint, mock_error_response):
    """Test that SmsException is raised when server returns an error."""
    with pytest.raises(SmsException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 404
