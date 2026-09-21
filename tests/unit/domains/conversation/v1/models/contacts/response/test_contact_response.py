from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)


def test_contact_response_expects_full_payload_parsed():
    """Test that a full payload validates and every field is read back."""
    contact = ContactResponse.model_validate(
        {
            "id": "01W4FFL35P4NC4K35CONTACT001",
            "channel_identities": [
                {
                    "channel": "MESSENGER",
                    "identity": "7968425018576406",
                    "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                },
                {"channel": "SMS", "identity": "12015555555", "app_id": ""},
            ],
            "channel_priority": ["MESSENGER", "SMS"],
            "display_name": "Marty McFly",
            "email": "time.traveler@delorean.com",
            "external_id": "external-1",
            "metadata": "Some metadata",
            "language": "EN_US",
        }
    )

    assert contact.id == "01W4FFL35P4NC4K35CONTACT001"
    assert contact.display_name == "Marty McFly"
    assert contact.email == "time.traveler@delorean.com"
    assert contact.external_id == "external-1"
    assert contact.metadata == "Some metadata"
    assert contact.language == "EN_US"
    assert contact.channel_priority == ["MESSENGER", "SMS"]
    assert len(contact.channel_identities) == 2
    assert contact.channel_identities[0].channel == "MESSENGER"
    assert (
        contact.channel_identities[0].app_id
        == "01W4FFL35P4NC4K35CONVAPP001"
    )
    assert contact.channel_identities[1].identity == "12015555555"


def test_contact_response_expects_all_fields_optional():
    """Test that every field defaults to None."""
    contact = ContactResponse()

    assert contact.id is None
    assert contact.channel_identities is None
    assert contact.channel_priority is None
    assert contact.display_name is None
    assert contact.email is None
    assert contact.external_id is None
    assert contact.language is None
    assert contact.metadata is None


def test_contact_response_expects_unknown_language_accepted():
    """Test that an unknown language value is accepted through the StrictStr fallback."""
    contact = ContactResponse(language="UNSPECIFIED")

    assert contact.language == "UNSPECIFIED"
