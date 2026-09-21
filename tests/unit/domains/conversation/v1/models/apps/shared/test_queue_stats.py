import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.apps.shared.queue_stats import (
    QueueStats,
)


def test_queue_stats_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = QueueStats(outbound_size=10, outbound_limit=500000)

    assert model.outbound_size == 10
    assert model.outbound_limit == 500000


def test_queue_stats_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = QueueStats()

    assert model.outbound_size is None
    assert model.outbound_limit is None
