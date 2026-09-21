import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.apps.shared.rate_limits import (
    RateLimits,
)


def test_rate_limits_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = RateLimits(inbound=25, outbound=25, events=25)

    assert model.inbound == 25
    assert model.outbound == 25
    assert model.events == 25


def test_rate_limits_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = RateLimits()

    assert model.inbound is None
    assert model.outbound is None
    assert model.events is None


def test_rate_limits_expects_accepts_webhooks_alias():
    """Test that event_destinations can be populated by its webhooks alias."""
    model = RateLimits(webhooks=30)

    assert model.events == 30


def test_rate_limits_expects_dump_uses_alias():
    """Test that model_dump(by_alias=True) emits the webhooks alias."""
    model = RateLimits(events=30)

    dumped = model.model_dump(by_alias=True, exclude_none=True)

    assert dumped == {"webhooks": 30}
