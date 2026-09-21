import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.contacts.internal.get_channel_profile_request import (
    GetChannelProfileRequest,
)
from sinch.domains.conversation.models.v1.messages.internal.request.recipient import (
    Recipient,
)


def test_get_channel_profile_request_expects_required_fields_parsed():
    """Test that app_id, recipient, and channel are read back correctly."""
    request = GetChannelProfileRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        recipient=Recipient(contact_id="01W4FFL35P4NC4K35CONTACT001"),
        channel="MESSENGER",
    )

    assert request.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert isinstance(request.recipient, Recipient)
    assert request.recipient.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert request.channel == "MESSENGER"


def test_get_channel_profile_request_expects_error_when_app_id_missing():
    """Test that app_id is required."""
    with pytest.raises(ValidationError):
        GetChannelProfileRequest(
            recipient=Recipient(contact_id="01W4FFL35P4NC4K35CONTACT001"),
            channel="MESSENGER",
        )


def test_get_channel_profile_request_expects_error_when_recipient_missing():
    """Test that recipient is required."""
    with pytest.raises(ValidationError):
        GetChannelProfileRequest(
            app_id="01W4FFL35P4NC4K35CONVAPP001", channel="MESSENGER"
        )


def test_get_channel_profile_request_expects_error_when_channel_missing():
    """Test that channel is required."""
    with pytest.raises(ValidationError):
        GetChannelProfileRequest(
            app_id="01W4FFL35P4NC4K35CONVAPP001",
            recipient=Recipient(contact_id="01W4FFL35P4NC4K35CONTACT001"),
        )
