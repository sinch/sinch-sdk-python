import pytest
from pydantic import ValidationError

from sinch.domains.sms.models.v1.response.group_response import GroupResponse
from sinch.domains.sms.models.v1.response.list_groups_response import ListGroupsResponse


def test_list_groups_response_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = ListGroupsResponse()

    assert model.count is None
    assert model.page is None
    assert model.page_size is None
    assert model.groups is None


def test_list_groups_response_expects_valid_input():
    """Test that the model correctly parses a full valid input."""
    model = ListGroupsResponse(
        count=1,
        page=0,
        page_size=10,
        groups=[{"id": "01FC66621XXXXX119Z8PMV1QPQ", "name": "Test Group", "size": 2}],
    )

    assert model.count == 1
    assert model.page == 0
    assert model.page_size == 10
    assert len(model.groups) == 1
    assert isinstance(model.groups[0], GroupResponse)
    assert model.groups[0].id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert model.groups[0].name == "Test Group"
    assert model.groups[0].size == 2


def test_list_groups_response_expects_empty_groups_list():
    """Test that an empty groups list is handled correctly."""
    model = ListGroupsResponse(count=0, page=0, page_size=10, groups=[])

    assert model.groups == []
    assert model.count == 0


def test_list_groups_response_expects_content_returns_groups():
    """Test that content property returns the groups list when populated."""
    model = ListGroupsResponse(
        groups=[{"id": "01FC66621XXXXX119Z8PMV1QPQ"}],
    )

    assert model.content == model.groups
    assert len(model.content) == 1


def test_list_groups_response_expects_content_returns_empty_list_when_no_groups():
    """Test that content property returns [] when groups is None."""
    model = ListGroupsResponse()

    assert model.content == []
