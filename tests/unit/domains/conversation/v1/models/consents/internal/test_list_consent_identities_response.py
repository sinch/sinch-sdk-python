from sinch.domains.conversation.models.v1.consents.internal.list_consent_identities_response import (
    ListConsentIdentitiesResponse,
)
from sinch.domains.conversation.models.v1.consents.response.consent_identity_response import (
    ConsentIdentityResponse,
)


def test_list_consent_identities_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListConsentIdentitiesResponse(
        identities=[{"identity": "33612345678"}],
        next_page_token="token",
    )

    assert len(model.identities) == 1
    assert isinstance(model.identities[0], ConsentIdentityResponse)
    assert model.identities[0].identity == "33612345678"
    assert model.next_page_token == "token"
    assert model.content == model.identities

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump == {
        "identities": [{"identity": "33612345678"}],
        "next_page_token": "token",
    }


def test_list_consent_identities_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ListConsentIdentitiesResponse()

    assert model.identities is None
    assert model.next_page_token is None


def test_list_consent_identities_response_expects_content_empty_when_identities_is_none():
    """Test that content returns an empty list when identities is None."""
    assert ListConsentIdentitiesResponse().content == []
