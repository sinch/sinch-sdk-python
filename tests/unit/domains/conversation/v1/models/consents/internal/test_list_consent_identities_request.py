import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.consents.internal.list_consent_identities_request import (
    ListConsentIdentitiesRequest,
)


def test_list_consent_identities_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListConsentIdentitiesRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        list_type="OPT_OUT_ALL",
        page_size=5,
        page_token="token_abc",
    )

    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.list_type == "OPT_OUT_ALL"
    assert model.page_size == 5
    assert model.page_token == "token_abc"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "list_type": "OPT_OUT_ALL",
        "page_size": 5,
        "page_token": "token_abc",
    }


def test_list_consent_identities_request_expects_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ListConsentIdentitiesRequest(
        app_id="APP123", list_type="OPT_OUT_ALL"
    )

    assert model.page_size is None
    assert model.page_token is None


def test_list_consent_identities_request_expects_unknown_list_type_accepted():
    """Test that a list type outside the known values is still accepted."""
    model = ListConsentIdentitiesRequest(
        app_id="APP123", list_type="OPT_OUT_FUTURE"
    )

    assert model.list_type == "OPT_OUT_FUTURE"


@pytest.mark.parametrize("missing", ["app_id", "list_type"])
def test_list_consent_identities_request_expects_missing_required_field_rejected(
    missing,
):
    """Test that the model rejects input missing a required field."""
    data = {"app_id": "APP123", "list_type": "OPT_OUT_ALL"}
    del data[missing]

    with pytest.raises(ValidationError):
        ListConsentIdentitiesRequest(**data)
