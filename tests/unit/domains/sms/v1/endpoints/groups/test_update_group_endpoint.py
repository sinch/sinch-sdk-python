import json
import pytest
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.sms.api.v1.exceptions import SmsException
from datetime import datetime, timezone

from sinch.domains.sms.api.v1.internal.groups_endpoints import UpdateGroupEndpoint
from sinch.domains.sms.models.v1.internal.update_group_request import UpdateGroupRequest
from sinch.domains.sms.models.v1.response.group_response import GroupResponse


@pytest.fixture
def request_data():
    return UpdateGroupRequest(group_id="01FC66621XXXXX119Z8PMV1QPQ", name="Updated Group")


@pytest.fixture
def mock_response():
    return HTTPResponse(
        status_code=200,
        body={
            "id": "01FC66621XXXXX119Z8PMV1QPQ",
            "name": "Updated Group",
            "size": 2,
            "created_at": "2024-06-06T09:22:14.304Z",
            "modified_at": "2024-06-06T09:22:48.054Z",
            "child_groups": ["01FC66621VHDBN119Z8PMV1AHY"],
            "auto_update": {
                "to": "+15551231234",
                "add": {"first_word": "JOIN"},
                "remove": {"first_word": "LEAVE"},
            },
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
    return UpdateGroupEndpoint("test_project_id", request_data)


def test_build_url(endpoint, mock_sinch_client_sms):
    """Test that the URL is built correctly."""
    assert (
        endpoint.build_url(mock_sinch_client_sms)
        == "https://zt.eu.sms.api.sinch.com/xms/v1/test_project_id/groups/01FC66621XXXXX119Z8PMV1QPQ"
    )


def test_handle_response_expects_correct_mapping(endpoint, mock_response):
    """Check if response is handled and mapped to the appropriate fields correctly."""
    parsed_response = endpoint.handle_response(mock_response)

    assert isinstance(parsed_response, GroupResponse)
    assert parsed_response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert parsed_response.name == "Updated Group"
    assert parsed_response.size == 2
    assert parsed_response.child_groups == ["01FC66621VHDBN119Z8PMV1AHY"]
    assert parsed_response.auto_update.to == "+15551231234"
    assert parsed_response.auto_update.add.first_word == "JOIN"
    assert parsed_response.auto_update.remove.first_word == "LEAVE"
    assert parsed_response.created_at == datetime(2024, 6, 6, 9, 22, 14, 304000, tzinfo=timezone.utc)
    assert parsed_response.modified_at == datetime(2024, 6, 6, 9, 22, 48, 54000, tzinfo=timezone.utc)


def test_handle_response_expects_sms_exception_on_error(endpoint, mock_error_response):
    """Test that SmsException is raised when server returns an error."""
    with pytest.raises(SmsException) as exc_info:
        endpoint.handle_response(mock_error_response)

    assert exc_info.value.is_from_server is True
    assert exc_info.value.http_response.status_code == 400


def test_request_body_excludes_none_fields(endpoint):
    """Test that None fields are excluded from the serialized request body."""
    body = json.loads(endpoint.request_body())

    assert body["name"] == "Updated Group"
    assert "group_id" not in body
    assert "add" not in body
    assert "remove" not in body
    assert "add_from_group" not in body
    assert "remove_from_group" not in body
    assert "auto_update" not in body


def test_request_body_expects_correct_serialization():
    """Test that all fields serialize correctly to the request body."""
    request_data = UpdateGroupRequest(
        group_id="01FC66621XXXXX119Z8PMV1QPQ",
        name="Updated Group",
        add=["+46701234567", "+46709876543"],
        remove=["+46701111111"],
        add_from_group="01FC66621VHDBN119Z8PMV1AHY",
        remove_from_group="01FC66621VHDBN119Z8PMV1AHZ",
        auto_update={"to": "+15551231234", "add": {"first_word": "JOIN"}, "remove": {"first_word": "LEAVE"}},
    )
    endpoint = UpdateGroupEndpoint("test_project_id", request_data)
    body = json.loads(endpoint.request_body())

    assert "group_id" not in body
    assert body["name"] == "Updated Group"
    assert body["add"] == ["+46701234567", "+46709876543"]
    assert body["remove"] == ["+46701111111"]
    assert body["add_from_group"] == "01FC66621VHDBN119Z8PMV1AHY"
    assert body["remove_from_group"] == "01FC66621VHDBN119Z8PMV1AHZ"
    assert body["auto_update"]["to"] == "+15551231234"
    assert body["auto_update"]["add"]["first_word"] == "JOIN"
    assert body["auto_update"]["remove"]["first_word"] == "LEAVE"
