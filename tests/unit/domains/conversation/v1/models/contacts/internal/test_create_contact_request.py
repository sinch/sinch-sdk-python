import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.contacts.internal import (
    CreateContactRequest,
)
from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)


def test_create_contact_request_expects_full_payload_parsed():
    """Test that a full payload validates and every field is read back."""
    request = CreateContactRequest(
        channel_identities=[{"channel": "SMS", "identity": "+12015555555"}],
        language="EN_US",
        channel_priority=["SMS"],
        display_name="Marty McFly",
        email="time.traveler@delorean.com",
        external_id="external-1",
        metadata="Some metadata",
    )

    assert request.channel_identities[0] == ChannelIdentity(
        channel="SMS", identity="+12015555555"
    )
    assert request.language == "EN_US"
    assert request.channel_priority == ["SMS"]
    assert request.display_name == "Marty McFly"
    assert request.email == "time.traveler@delorean.com"
    assert request.external_id == "external-1"
    assert request.metadata == "Some metadata"


def test_create_contact_request_expects_optional_fields_default_to_none():
    """Test that the optional fields default to None."""
    request = CreateContactRequest(
        channel_identities=[{"channel": "SMS", "identity": "+12015555555"}],
        language="EN_US",
    )

    assert request.channel_priority is None
    assert request.display_name is None
    assert request.email is None
    assert request.external_id is None
    assert request.metadata is None


def test_create_contact_request_expects_error_when_required_fields_missing():
    """Test that channel_identities and language are required."""
    with pytest.raises(ValidationError):
        CreateContactRequest(language="EN_US")

    with pytest.raises(ValidationError):
        CreateContactRequest(
            channel_identities=[
                {"channel": "SMS", "identity": "+12015555555"}
            ]
        )