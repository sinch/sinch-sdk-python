import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.apps.shared.dispatch_retention_policy import (
    DispatchRetentionPolicy,
)


def test_dispatch_retention_policy_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = DispatchRetentionPolicy(
        retention_type="MESSAGE_EXPIRE_POLICY",
        ttl_days=7,
    )

    assert model.retention_type == "MESSAGE_EXPIRE_POLICY"
    assert model.ttl_days == 7


def test_dispatch_retention_policy_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = DispatchRetentionPolicy()

    assert model.retention_type is None
    assert model.ttl_days is None
