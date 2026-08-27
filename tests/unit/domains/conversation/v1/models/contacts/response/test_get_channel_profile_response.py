from sinch.domains.conversation.models.v1.contacts.response.get_channel_profile_response import (
    GetChannelProfileResponse,
)


def test_get_channel_profile_response_expects_profile_name_parsed():
    """Test that profile_name is read back correctly."""
    response = GetChannelProfileResponse.model_validate(
        {"profile_name": "Marty McFly FB"}
    )

    assert response.profile_name == "Marty McFly FB"


def test_get_channel_profile_response_expects_optional_field_defaults_to_none():
    """Test that profile_name defaults to None."""
    response = GetChannelProfileResponse()

    assert response.profile_name is None
