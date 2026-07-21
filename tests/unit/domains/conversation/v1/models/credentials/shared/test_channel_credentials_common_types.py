from sinch.domains.conversation.models.v1.credentials.shared.channel_credentials_common_types import (
    ChannelCredentialsCommonTypes,
)
from sinch.domains.conversation.models.v1.credentials.shared.channel_integration_state import (
    ChannelIntegrationState,
)


def test_channel_credentials_common_types_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = ChannelCredentialsCommonTypes()

    assert model.callback_secret is None
    assert model.channel is None
    assert model.state is None
    assert model.channel_known_id is None
    assert model.credential_ordinal_number is None


def test_channel_credentials_common_types_expects_parsed_input():
    """Test that the model correctly parses a full valid input, including nested state."""
    model = ChannelCredentialsCommonTypes(
        callback_secret="secret",
        channel="SMS",
        state={"status": "ACTIVE", "description": "ok"},
        channel_known_id="known-id",
        credential_ordinal_number=0,
    )

    assert model.callback_secret == "secret"
    assert model.channel == "SMS"
    assert isinstance(model.state, ChannelIntegrationState)
    assert model.state.status == "ACTIVE"
    assert model.channel_known_id == "known-id"
    assert model.credential_ordinal_number == 0
