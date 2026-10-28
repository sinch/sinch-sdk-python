import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.inbound.reaction_event import (
    ReactionEvent,
)


def test_reaction_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ReactionEvent(
        emoji="thumbs_up",
        action="REACTION_ACTION_REACT",
        message_id="message-1",
        reaction_category="like",
    )

    assert model.emoji == "thumbs_up"
    assert model.action == "REACTION_ACTION_REACT"
    assert model.message_id == "message-1"
    assert model.reaction_category == "like"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["emoji"] == "thumbs_up"
    assert alias_dump["action"] == "REACTION_ACTION_REACT"
    assert alias_dump["message_id"] == "message-1"
    assert alias_dump["reaction_category"] == "like"


def test_reaction_event_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ReactionEvent(
        emoji="thumbs_up",
        action="REACTION_ACTION_REACT",
        message_id="message-1",
    )

    assert model.reaction_category is None


@pytest.mark.parametrize("missing", ["emoji", "action", "message_id"])
def test_reaction_event_expects_validation_error_for_missing_required(missing):
    """Test that emoji, action and message_id are required."""
    payload = {
        "emoji": "thumbs_up",
        "action": "REACTION_ACTION_REACT",
        "message_id": "message-1",
    }
    del payload[missing]

    with pytest.raises(ValidationError):
        ReactionEvent(**payload)
