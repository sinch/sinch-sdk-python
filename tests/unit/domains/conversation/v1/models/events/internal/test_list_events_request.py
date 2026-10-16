from sinch.domains.conversation.models.v1.events.internal.list_events_request import (
    ListEventsRequest,
)


def test_list_events_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListEventsRequest(
        conversation_id="01W4FFL35P4NC4K35CONVERS001",
        contact_id="01W4FFL35P4NC4K35CONTACT001",
        page_size=10,
        page_token="token",
    )

    assert model.conversation_id == "01W4FFL35P4NC4K35CONVERS001"
    assert model.contact_id == "01W4FFL35P4NC4K35CONTACT001"
    assert model.page_size == 10
    assert model.page_token == "token"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["conversation_id"] == "01W4FFL35P4NC4K35CONVERS001"
    assert alias_dump["contact_id"] == "01W4FFL35P4NC4K35CONTACT001"
    assert alias_dump["page_size"] == 10
    assert alias_dump["page_token"] == "token"


def test_list_events_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ListEventsRequest()

    assert model.conversation_id is None
    assert model.contact_id is None
    assert model.page_size is None
    assert model.page_token is None
