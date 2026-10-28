from sinch.domains.conversation.models.v1.capability.response.lookup_capability_response import (
    LookupCapabilityResponse,
)


def test_lookup_capability_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = LookupCapabilityResponse(
        app_id="01W4FFL35P4NC4K35CONVAPP001",
        recipient={"contact_id": "01W4FFL35P4NC4K35CONTACT001"},
        request_id="01W4FFL35P4NC4K35CAPABILITY",
    )

    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.recipient.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert model.request_id == "01W4FFL35P4NC4K35CAPABILITY"

    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["app_id"] == "01W4FFL35P4NC4K35CONVAPP001"
    assert alias_dump["request_id"] == "01W4FFL35P4NC4K35CAPABILITY"


def test_lookup_capability_response_expects_all_optionals_default_to_none():
    """Test that every field defaults to None."""
    model = LookupCapabilityResponse()

    assert model.app_id is None
    assert model.recipient is None
    assert model.request_id is None
