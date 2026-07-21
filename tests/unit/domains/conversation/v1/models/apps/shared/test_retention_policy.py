import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.apps.shared.retention_policy import (
    RetentionPolicy,
)


@pytest.mark.parametrize(
    "retention_type",
    [
        "MESSAGE_EXPIRE_POLICY",
        "CONVERSATION_EXPIRE_POLICY",
        "PERSIST_RETENTION_POLICY",
        "UNEXPECTED_VALUE",
    ],
)
def test_retention_policy_expects_parsed_input(retention_type):
    """Test that the model correctly parses a full valid input."""
    model = RetentionPolicy(retention_type=retention_type, ttl_days=180)

    assert model.retention_type == retention_type
    assert model.ttl_days == 180


def test_retention_policy_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = RetentionPolicy()

    assert model.retention_type is None
    assert model.ttl_days is None
