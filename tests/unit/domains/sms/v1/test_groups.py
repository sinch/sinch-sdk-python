import pytest
from sinch.core.pagination import SMSPaginator
from sinch.domains.sms.api.v1.groups_apis import Groups
from sinch.domains.sms.api.v1.internal.groups_endpoints import CreateGroupEndpoint, DeleteGroupEndpoint, GetGroupEndpoint, ListGroupMembersEndpoint, ListGroupsEndpoint, ReplaceGroupEndpoint, UpdateGroupEndpoint
from sinch.domains.sms.models.v1.response.group_response import GroupResponse
from sinch.domains.sms.models.v1.response.list_groups_response import ListGroupsResponse

@pytest.fixture
def mock_group_response():
    """Sample GroupResponse for testing."""
    return GroupResponse(
        id="01FC66621XXXXX119Z8PMV1QPQ",
    )


def test_groups_create_correct_request(
    mock_sinch_client_sms, mocker, mock_group_response
):
    """Test that create sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = mock_group_response

    spy_endpoint = mocker.spy(CreateGroupEndpoint, "__init__")

    groups = Groups(mock_sinch_client_sms)
    response = groups.create(
        name="Test Group",
        members=["+46701234567", "+46709876543"],
        child_groups=["01FC66621VHDBN119Z8PMV1AHY"],
        auto_update={"to": "+15551231234", "add": {"first_word": "JOIN"}, "remove": {"first_word": "LEAVE"}},
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].name == "Test Group"
    assert kwargs["request_data"].members == ["+46701234567", "+46709876543"]
    assert kwargs["request_data"].child_groups == ["01FC66621VHDBN119Z8PMV1AHY"]
    assert kwargs["request_data"].auto_update.to == "+15551231234"
    assert kwargs["request_data"].auto_update.add.first_word == "JOIN"
    assert kwargs["request_data"].auto_update.remove.first_word == "LEAVE"

    assert isinstance(response, GroupResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_groups_list_correct_request(mock_sinch_client_sms, mocker):
    """Test that list sends the correct request and handles the response properly."""

    mock_list_response = ListGroupsResponse(count=0, page=1, page_size=0, groups=[])

    mock_sinch_client_sms.configuration.transport.request.return_value = mock_list_response

    spy_endpoint = mocker.spy(ListGroupsEndpoint, "__init__")

    groups = Groups(mock_sinch_client_sms)

    response = groups.list(
        page=0,
        page_size=10
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].page == 0
    assert kwargs["request_data"].page_size == 10


    assert isinstance(response, SMSPaginator)
    assert hasattr(response, "has_next_page")
    assert response.result == mock_list_response
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_groups_get_correct_request(mock_sinch_client_sms, mocker, mock_group_response):
    """Test that get sends the correct request and handles the response properly."""

    mock_sinch_client_sms.configuration.transport.request.return_value = mock_group_response

    spy_endpoint = mocker.spy(GetGroupEndpoint, "__init__")

    groups = Groups(mock_sinch_client_sms)

    response = groups.get(group_id="01FC66621XXXXX119Z8PMV1QPQ")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].group_id == "01FC66621XXXXX119Z8PMV1QPQ"


    assert isinstance(response, GroupResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_groups_replace_correct_request(mock_sinch_client_sms, mocker, mock_group_response):
    """Test that replace sends the correct request and handles the response properly."""

    mock_sinch_client_sms.configuration.transport.request.return_value = mock_group_response

    spy_endpoint = mocker.spy(ReplaceGroupEndpoint, "__init__")

    groups = Groups(mock_sinch_client_sms)

    response = groups.replace(
        group_id="01FC66621XXXXX119Z8PMV1QPQ",
        name="Replaced Group",
        members=["+46701234567", "+46709876543"],
        child_groups=["01FC66621VHDBN119Z8PMV1AHY"],
        auto_update={"to": "+15551231234", "add": {"first_word": "JOIN"}, "remove": {"first_word": "LEAVE"}},
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].group_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert kwargs["request_data"].name == "Replaced Group"
    assert kwargs["request_data"].members == ["+46701234567", "+46709876543"]
    assert kwargs["request_data"].child_groups == ["01FC66621VHDBN119Z8PMV1AHY"]
    assert kwargs["request_data"].auto_update.to == "+15551231234"
    assert kwargs["request_data"].auto_update.add.first_word == "JOIN"
    assert kwargs["request_data"].auto_update.remove.first_word == "LEAVE"

    assert isinstance(response, GroupResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_groups_update_correct_request(mock_sinch_client_sms, mocker, mock_group_response):
    """Test that update sends the correct request and handles the response properly."""

    mock_sinch_client_sms.configuration.transport.request.return_value = mock_group_response

    spy_endpoint = mocker.spy(UpdateGroupEndpoint, "__init__")

    groups = Groups(mock_sinch_client_sms)

    response = groups.update(
        group_id="01FC66621XXXXX119Z8PMV1QPQ",
        name="Updated Group",
        add=["+46701234567", "+46709876543"],
        remove=["+46701111111"],
        add_from_group="01FC66621VHDBN119Z8PMV1AHY",
        remove_from_group="01FC66621VHDBN119Z8PMV1AHZ",
        auto_update={"to": "+15551231234", "add": {"first_word": "JOIN"}, "remove": {"first_word": "LEAVE"}},
    )

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].group_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert kwargs["request_data"].name == "Updated Group"
    assert kwargs["request_data"].add == ["+46701234567", "+46709876543"]
    assert kwargs["request_data"].remove == ["+46701111111"]
    assert kwargs["request_data"].add_from_group == "01FC66621VHDBN119Z8PMV1AHY"
    assert kwargs["request_data"].remove_from_group == "01FC66621VHDBN119Z8PMV1AHZ"
    assert kwargs["request_data"].auto_update.to == "+15551231234"
    assert kwargs["request_data"].auto_update.add.first_word == "JOIN"
    assert kwargs["request_data"].auto_update.remove.first_word == "LEAVE"

    assert isinstance(response, GroupResponse)
    assert response.id == "01FC66621XXXXX119Z8PMV1QPQ"
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_groups_delete_correct_request(mock_sinch_client_sms, mocker):
    """Test that delete sends the correct request and handles the response properly."""
    mock_sinch_client_sms.configuration.transport.request.return_value = None

    spy_endpoint = mocker.spy(DeleteGroupEndpoint, "__init__")

    groups = Groups(mock_sinch_client_sms)
    response = groups.delete(group_id="01FC66621XXXXX119Z8PMV1QPQ")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].group_id == "01FC66621XXXXX119Z8PMV1QPQ"

    assert response is None
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()


def test_groups_list_members_correct_request(mock_sinch_client_sms, mocker):
    """Test that list_members sends the correct request and returns an SMSPaginator."""
    from sinch.domains.sms.models.v1.response.list_group_members_response import ListGroupMembersResponse

    mock_members_response = ListGroupMembersResponse(members=["+46701234567", "+46709876543"])
    mock_sinch_client_sms.configuration.transport.request.return_value = mock_members_response

    spy_endpoint = mocker.spy(ListGroupMembersEndpoint, "__init__")

    groups = Groups(mock_sinch_client_sms)
    response = groups.list_members(group_id="01FC66621XXXXX119Z8PMV1QPQ")

    spy_endpoint.assert_called_once()
    _, kwargs = spy_endpoint.call_args

    assert kwargs["project_id"] == "test_project_id"
    assert kwargs["request_data"].group_id == "01FC66621XXXXX119Z8PMV1QPQ"

    assert isinstance(response, SMSPaginator)
    assert hasattr(response, "has_next_page")
    assert response.has_next_page is False
    assert response.result == mock_members_response
    assert response.content() == ["+46701234567", "+46709876543"]
    mock_sinch_client_sms.configuration.transport.request.assert_called_once()
