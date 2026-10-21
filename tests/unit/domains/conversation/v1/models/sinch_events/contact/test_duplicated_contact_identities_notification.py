from sinch.domains.conversation.models.v1.sinch_events.contact.duplicated_contact_identities_notification import (
    DuplicatedContactIdentitiesNotification,
)
from sinch.domains.conversation.models.v1.sinch_events.contact.duplicated_identities import (
    DuplicatedIdentities,
)


def test_duplicated_contact_identities_notification_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = DuplicatedContactIdentitiesNotification(
        duplicated_identities=[
            {"channel": "SMS", "contact_ids": ["contact-1", "contact-2"]},
            {"channel": "MMS", "contact_ids": ["contact-3", "contact-4"]},
        ]
    )

    assert len(model.duplicated_identities) == 2
    assert isinstance(model.duplicated_identities[0], DuplicatedIdentities)
    assert model.duplicated_identities[0].channel == "SMS"
    assert model.duplicated_identities[1].contact_ids == ["contact-3", "contact-4"]

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["duplicated_identities"] == [
        {"channel": "SMS", "contact_ids": ["contact-1", "contact-2"]},
        {"channel": "MMS", "contact_ids": ["contact-3", "contact-4"]},
    ]


def test_duplicated_contact_identities_notification_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = DuplicatedContactIdentitiesNotification()

    assert model.duplicated_identities is None
