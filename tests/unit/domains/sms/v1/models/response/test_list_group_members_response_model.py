import pytest
from pydantic import ValidationError

from sinch.domains.sms.models.v1.response.list_group_members_response import ListGroupMembersResponse


def test_list_group_members_response_expects_valid_input():
    """Test that the model correctly parses a list of MSISDNs."""
    model = ListGroupMembersResponse(members=["+46701234567", "+46709876543"])

    assert model.members == ["+46701234567", "+46709876543"]


def test_list_group_members_response_expects_content_returns_members():
    """Test that content property returns the members list."""
    model = ListGroupMembersResponse(members=["+46701234567"])

    assert model.content == model.members


def test_list_group_members_response_expects_empty_members_list():
    """Test that an empty members list is handled correctly."""
    model = ListGroupMembersResponse(members=[])

    assert model.members == []
    assert model.content == []


def test_list_group_members_response_expects_no_pagination_fields():
    """Test that count, page, page_size are absent so SMSPaginator sets has_next_page=False."""
    model = ListGroupMembersResponse(members=["+46701234567"])

    assert getattr(model, "count", None) is None
    assert getattr(model, "page", None) is None
    assert getattr(model, "page_size", None) is None


def test_list_group_members_response_expects_strict_str_rejects_non_string():
    """Test that non-string members are rejected."""
    with pytest.raises(ValidationError):
        ListGroupMembersResponse(members=[123])
