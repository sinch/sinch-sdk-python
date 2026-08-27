from sinch.domains.conversation.models.v1.contacts.internal.list_identity_conflicts_request import (
    ListIdentityConflictsRequest,
)


def test_list_identity_conflicts_request_expects_fields_parsed():
    """Test that page_size and page_token are read back correctly."""
    request = ListIdentityConflictsRequest(page_size=10, page_token="a-token")

    assert request.page_size == 10
    assert request.page_token == "a-token"


def test_list_identity_conflicts_request_expects_optional_fields_default_to_none():
    """Test that both fields default to None."""
    request = ListIdentityConflictsRequest()

    assert request.page_size is None
    assert request.page_token is None
