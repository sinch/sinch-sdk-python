from sinch.domains.conversation.models.v1.contacts.internal.list_contacts_response import (
    ListContactsResponse,
)
from sinch.domains.conversation.models.v1.contacts.response.contact_response import (
    ContactResponse,
)


def test_list_contacts_response_expects_full_payload_parsed():
    """Test that a full payload validates and every field is read back."""
    response = ListContactsResponse.model_validate(
        {
            "contacts": [
                {
                    "id": "01W4FFL35P4NC4K35CONTACT001",
                    "display_name": "Marty McFly",
                },
                {
                    "id": "01W4FFL35P4NC4K35CONTACT002",
                    "display_name": "Pika pika",
                },
            ],
            "next_page_token": "ChowMVc0RkZMMzVQNE5DNEszNUNPTlRBQ1QwMDI=",
        }
    )

    assert (
        response.next_page_token
        == "ChowMVc0RkZMMzVQNE5DNEszNUNPTlRBQ1QwMDI="
    )
    assert len(response.contacts) == 2
    assert isinstance(response.contacts[0], ContactResponse)
    assert response.contacts[0].id == "01W4FFL35P4NC4K35CONTACT001"
    assert response.contacts[1].display_name == "Pika pika"


def test_list_contacts_response_expects_optional_fields_default_to_none():
    """Test that both fields default to None."""
    response = ListContactsResponse()

    assert response.contacts is None
    assert response.next_page_token is None


def test_list_contacts_response_expects_content_empty_when_contacts_is_none():
    """Test that content returns an empty list when contacts is None."""
    assert ListContactsResponse().content == []


def test_list_contacts_response_expects_content_returns_items():
    """Test that content returns the contacts when present."""
    response = ListContactsResponse(
        contacts=[ContactResponse(id="01W4FFL35P4NC4K35CONTACT001")]
    )

    assert response.content == response.contacts
    assert len(response.content) == 1
