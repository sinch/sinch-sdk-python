import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)


def test_channel_identity_expects_full_payload_parsed():
    """Test that a full payload validates and every field is read back."""
    identity = ChannelIdentity(
        channel="MESSENGER",
        identity="7968425018576406",
        app_id="01W4FFL35P4NC4K35CONVAPP001",
    )

    assert identity.channel == "MESSENGER"
    assert identity.identity == "7968425018576406"
    assert identity.app_id == "01W4FFL35P4NC4K35CONVAPP001"


def test_channel_identity_expects_app_id_optional():
    """Test that app_id defaults to None."""
    identity = ChannelIdentity(channel="SMS", identity="+12015555555")

    assert identity.app_id is None


def test_channel_identity_expects_unknown_channel_accepted():
    """Test that an unknown channel value is accepted through the StrictStr fallback."""
    identity = ChannelIdentity(channel="A_NEW_CHANNEL", identity="+1")

    assert identity.channel == "A_NEW_CHANNEL"


def test_channel_identity_expects_dump_by_alias():
    """Test that the model dumps the wire field names."""
    identity = ChannelIdentity(channel="SMS", identity="+12015555555")

    assert identity.model_dump(by_alias=True, exclude_unset=True) == {
        "channel": "SMS",
        "identity": "+12015555555",
    }


def test_channel_identity_expects_error_when_required_field_missing():
    """Test that identity is required."""
    with pytest.raises(ValidationError):
        ChannelIdentity(channel="SMS")
