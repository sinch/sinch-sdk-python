from sinch.domains.conversation.models.v1.contacts.internal import (
    ListContactsRequest,
)


def test_list_contacts_request_expects_full_payload_parsed():
    """Test that a full payload validates and every field is read back."""
    request = ListContactsRequest(
        page_size=10,
        page_token="a-token",
        external_id="external-1",
        channel="SMS",
        identity="+12015555555",
    )

    assert request.page_size == 10
    assert request.page_token == "a-token"
    assert request.external_id == "external-1"
    assert request.channel == "SMS"
    assert request.identity == "+12015555555"


def test_list_contacts_request_expects_all_fields_optional():
    """Test that every field defaults to None."""
    request = ListContactsRequest()

    assert request.page_size is None
    assert request.page_token is None
    assert request.external_id is None
    assert request.channel is None
    assert request.identity is None


def test_list_contacts_request_expects_unknown_channel_accepted():
    """Test that an unknown channel value is accepted through the StrictStr fallback."""
    request = ListContactsRequest(channel="A_NEW_CHANNEL")

    assert request.channel == "A_NEW_CHANNEL"
