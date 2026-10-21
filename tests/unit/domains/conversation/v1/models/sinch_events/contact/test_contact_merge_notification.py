from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.contact_merge_notification import (
    ContactMergeNotification,
)


def test_contact_merge_notification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ContactMergeNotification(
        preserved_contact={"id": "contact-2", "display_name": "Destination"},
        deleted_contact={"id": "contact-1", "display_name": "Source"},
    )

    assert isinstance(model.preserved_contact, ContactResponse)
    assert model.preserved_contact.id == "contact-2"
    assert model.preserved_contact.display_name == "Destination"
    assert isinstance(model.deleted_contact, ContactResponse)
    assert model.deleted_contact.id == "contact-1"
    assert model.deleted_contact.display_name == "Source"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["preserved_contact"] == {
        "id": "contact-2",
        "display_name": "Destination",
    }
    assert alias_dump["deleted_contact"] == {
        "id": "contact-1",
        "display_name": "Source",
    }


def test_contact_merge_notification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ContactMergeNotification()

    assert model.preserved_contact is None
    assert model.deleted_contact is None
