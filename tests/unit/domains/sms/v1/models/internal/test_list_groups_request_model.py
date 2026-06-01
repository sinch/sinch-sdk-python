import pytest
from pydantic import ValidationError

from sinch.domains.sms.models.v1.internal.list_groups_request import ListGroupsRequest


def test_list_groups_request_expects_defaults():
    """Test that all optional fields default to None."""
    model = ListGroupsRequest()

    assert model.page is None
    assert model.page_size is None


def test_list_groups_request_expects_parsed_input():
    """Test that the model correctly parses page and page_size."""
    model = ListGroupsRequest(page=1, page_size=10)

    assert model.page == 1
    assert model.page_size == 10


def test_list_groups_request_expects_strict_int_rejects_str():
    """Test that StrictInt fields reject string values."""
    with pytest.raises(ValidationError):
        ListGroupsRequest(page="one")

    with pytest.raises(ValidationError):
        ListGroupsRequest(page_size="ten")
