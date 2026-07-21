import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.apps.shared.message_retry_settings import (
    MessageRetrySettings,
)


def test_message_retry_settings_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = MessageRetrySettings(retry_duration=300)

    assert model.retry_duration == 300


def test_message_retry_settings_expects_retry_duration_defaults_to_none():
    """Test that the optional retry_duration field defaults to None."""
    model = MessageRetrySettings()

    assert model.retry_duration is None
