import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.events.shared.agent_left_event import (
    AgentLeftEvent,
)


def test_agent_left_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = AgentLeftEvent(
        agent={
            "display_name": "Agent Smith",
            "type": "HUMAN",
            "picture_url": "https://example.com/agent.png",
        }
    )

    assert model.agent.display_name == "Agent Smith"
    assert model.agent.type == "HUMAN"
    assert model.agent.picture_url == "https://example.com/agent.png"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["agent"]["display_name"] == "Agent Smith"
    assert alias_dump["agent"]["type"] == "HUMAN"
    assert alias_dump["agent"]["picture_url"] == "https://example.com/agent.png"


def test_agent_left_event_expects_agent_optionals_default_to_none():
    """Test that an agent without any detail is accepted."""
    model = AgentLeftEvent(agent={})

    assert model.agent.display_name is None
    assert model.agent.type is None
    assert model.agent.picture_url is None


def test_agent_left_event_expects_validation_error_for_missing_required():
    """Test that agent is required."""
    with pytest.raises(ValidationError):
        AgentLeftEvent()
