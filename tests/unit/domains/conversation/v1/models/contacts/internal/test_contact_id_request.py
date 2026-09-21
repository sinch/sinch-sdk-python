import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.contacts.internal import (
    ContactIdRequest,
)


def test_contact_id_request_expects_contact_id_parsed():
    """Test that contact_id is read back correctly."""
    request = ContactIdRequest(contact_id="01W4FFL35P4NC4K35CONTACT001")

    assert request.contact_id == "01W4FFL35P4NC4K35CONTACT001"


def test_contact_id_request_expects_error_when_contact_id_missing():
    """Test that contact_id is required."""
    with pytest.raises(ValidationError):
        ContactIdRequest()
