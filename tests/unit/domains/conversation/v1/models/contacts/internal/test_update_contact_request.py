import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.contacts.internal import (
    UpdateContactRequest,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)


def test_update_contact_request_expects_full_payload_parsed():
    """Test that a full payload validates and every field is read back."""
    request = UpdateContactRequest(
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        channel_identities=[
            {
                "channel": "MESSENGER",
                "identity": "7968425018576406",
                "app_id": "01W4FFL35P4NC4K35CONVAPP001",
            }
        ],
        channel_priority=["MESSENGER"],
        display_name="Marty McFly",
        email="time.traveler@delorean.com",
        external_id="external-1",
        language="FR",
        metadata="Some metadata",
    )

    assert request.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert isinstance(request.channel_identities[0], ChannelIdentity)
    assert request.channel_identities[0] == ChannelIdentity(
        channel="MESSENGER",
        identity="7968425018576406",
        app_id="01W4FFL35P4NC4K35CONVAPP001",
    )
    assert request.channel_priority == ["MESSENGER"]
    assert request.display_name == "Marty McFly"
    assert request.email == "time.traveler@delorean.com"
    assert request.external_id == "external-1"
    assert request.language == "FR"
    assert request.metadata == "Some metadata"


def test_update_contact_request_expects_optional_fields_default_to_none():
    """Test that every field but contact_id defaults to None."""
    request = UpdateContactRequest(
        contact_id="01W4FFL35P4NC4K35CONTACT001"
    )

    assert request.channel_identities is None
    assert request.channel_priority is None
    assert request.display_name is None
    assert request.email is None
    assert request.external_id is None
    assert request.language is None
    assert request.metadata is None


def test_update_contact_request_expects_error_when_contact_id_missing():
    """Test that contact_id is required."""
    with pytest.raises(ValidationError):
        UpdateContactRequest(display_name="Marty McFly")
