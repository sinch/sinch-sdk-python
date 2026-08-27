def test_contact_identity_conflict_expects_full_payload_parsed():
    """Test that a full payload validates and every field is read back."""
    from sinch.domains.conversation.models.v1.contacts.response.contact_identity_conflict import (
        ContactIdentityConflict,
    )

    conflict = ContactIdentityConflict.model_validate(
        {
            "identity": "12015555555",
            "channels": ["RCS", "SMS"],
            "contact_ids": [
                "01W4FFL35P4NC4K35CONTACT001",
                "01W4FFL35P4NC4K35CONTACT002",
            ],
        }
    )

    assert conflict.identity == "12015555555"
    assert conflict.channels == ["RCS", "SMS"]
    assert conflict.contact_ids == [
        "01W4FFL35P4NC4K35CONTACT001",
        "01W4FFL35P4NC4K35CONTACT002",
    ]


def test_contact_identity_conflict_expects_optional_fields_default_to_none():
    """Test that all fields default to None."""
    from sinch.domains.conversation.models.v1.contacts.response.contact_identity_conflict import (
        ContactIdentityConflict,
    )

    conflict = ContactIdentityConflict()

    assert conflict.identity is None
    assert conflict.channels is None
    assert conflict.contact_ids is None
