import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.capability.internal.lookup_capability_request import (
    LookupCapabilityRequest,
)


def test_lookup_capability_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = LookupCapabilityRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        recipient={"contact_id": "01W4FFL35P4NC4K35CONTACT001"},
        request_id="01W4FFL35P4NC4K35CAPABILITY",
    )

    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.recipient.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert model.request_id == "01W4FFL35P4NC4K35CAPABILITY"

    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "01W4FFL35P4NC4K35CONVAPP001"
    assert alias_dump["recipient"] == {
        "contact_id": "01W4FFL35P4NC4K35CONTACT001"
    }
    assert alias_dump["request_id"] == "01W4FFL35P4NC4K35CAPABILITY"


def test_lookup_capability_request_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = LookupCapabilityRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        recipient={"contact_id": "01W4FFL35P4NC4K35CONTACT001"},
    )

    assert model.request_id is None


def test_lookup_capability_request_expects_missing_required_field_rejected():
    """Test that the model rejects input missing a required field."""
    with pytest.raises(ValidationError):
        LookupCapabilityRequest(
            recipient={"contact_id": "01W4FFL35P4NC4K35CONTACT001"}
        )
