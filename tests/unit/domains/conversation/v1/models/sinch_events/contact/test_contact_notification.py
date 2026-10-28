from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_notification import (
    ContactNotification,
)


def test_contact_notification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ContactNotification(
        contact={
            "id": "01W4FFL35P4NC4K35CONTACT01",
            "display_name": "Source Contact",
            "channel_identities": [{"channel": "SMS", "identity": "12015555555"}],
        }
    )

    assert isinstance(model.contact, ContactResponse)
    assert model.contact.id == "01W4FFL35P4NC4K35CONTACT01"
    assert model.contact.display_name == "Source Contact"
    assert model.contact.channel_identities[0].identity == "12015555555"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["contact"] == {
        "id": "01W4FFL35P4NC4K35CONTACT01",
        "display_name": "Source Contact",
        "channel_identities": [{"channel": "SMS", "identity": "12015555555"}],
    }


def test_contact_notification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ContactNotification()

    assert model.contact is None
