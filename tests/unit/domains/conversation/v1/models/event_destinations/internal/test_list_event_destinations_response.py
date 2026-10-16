from sinch.domains.conversation.models.v1.event_destinations.internal.list_event_destinations_response import (
    ListEventDestinationsResponse,
)
from sinch.domains.conversation.models.v1.event_destinations.response.event_destination_response import (
    EventDestinationResponse,
)


def test_list_event_destinations_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListEventDestinationsResponse(
        webhooks=[
            {"id": "01W4FFL35P4NC4K35WEBHOOK001", "target": "https://a.com"},
            {"id": "01W4FFL35P4NC4K35WEBHOOK002", "target": "https://b.com"},
        ]
    )

    assert len(model.event_destinations) == 2
    assert isinstance(model.event_destinations[0], EventDestinationResponse)
    assert model.event_destinations[1].target == "https://b.com"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["webhooks"][0]["id"] == "01W4FFL35P4NC4K35WEBHOOK001"


def test_list_event_destinations_response_expects_all_optionals_default_to_none():
    """Test that optional fields default to None."""
    model = ListEventDestinationsResponse()

    assert model.event_destinations is None


def test_list_event_destinations_response_expects_content_empty_when_list_is_none():
    """Test that content returns an empty list when the list field is None."""
    assert ListEventDestinationsResponse().content == []

