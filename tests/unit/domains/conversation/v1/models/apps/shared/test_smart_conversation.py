import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.apps.shared.smart_conversation import (
    SmartConversation,
)


def test_smart_conversation_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SmartConversation(enabled=True)

    assert model.enabled is True


def test_smart_conversation_expects_enabled_defaults_to_none():
    """Test that the optional enabled field defaults to None."""
    model = SmartConversation()

    assert model.enabled is None
