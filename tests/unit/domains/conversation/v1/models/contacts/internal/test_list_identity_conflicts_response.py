from sinch.domains.conversation.models.v1.contacts.internal.list_identity_conflicts_response import (
    ListIdentityConflictsResponse,
)
from sinch.domains.conversation.models.v1.contacts.response.contact_identity_conflict import (
    ContactIdentityConflict,
)


def test_list_identity_conflicts_response_expects_full_payload_parsed():
    """Test that a full payload validates and every field is read back."""
    response = ListIdentityConflictsResponse.model_validate(
        {
            "conflicts": [
                {
                    "identity": "12015555555",
                    "channels": ["RCS", "SMS"],
                    "contact_ids": [
                        "01W4FFL35P4NC4K35CONTACT001",
                        "01W4FFL35P4NC4K35CONTACT002",
                    ],
                },
            ],
            "next_page_token": "MTIwMTY2NjY2NjY=",
        }
    )

    assert response.next_page_token == "MTIwMTY2NjY2NjY="
    assert len(response.conflicts) == 1
    assert isinstance(response.conflicts[0], ContactIdentityConflict)
    assert response.conflicts[0].identity == "12015555555"
    assert response.conflicts[0].channels == ["RCS", "SMS"]
    assert response.conflicts[0].contact_ids == [
        "01W4FFL35P4NC4K35CONTACT001",
        "01W4FFL35P4NC4K35CONTACT002",
    ]


def test_list_identity_conflicts_response_expects_optional_fields_default_to_none():
    """Test that both fields default to None."""
    response = ListIdentityConflictsResponse()

    assert response.conflicts is None
    assert response.next_page_token is None


def test_list_identity_conflicts_response_expects_content_empty_when_conflicts_is_none():
    """Test that content returns an empty list when conflicts is None."""
    assert ListIdentityConflictsResponse().content == []


def test_list_identity_conflicts_response_expects_content_returns_items():
    """Test that content returns the conflicts when present."""
    response = ListIdentityConflictsResponse(
        conflicts=[ContactIdentityConflict(identity="12015555555")]
    )

    assert response.content == response.conflicts
    assert len(response.content) == 1
