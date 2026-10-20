import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.consents.response.consent_identity_response import (
    ConsentIdentityResponse,
)


def test_consent_identity_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ConsentIdentityResponse(identity="33612345678")

    assert model.identity == "33612345678"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {"identity": "33612345678"}


def test_consent_identity_response_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        ConsentIdentityResponse()
