import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.sinch_events.inbound.comment_event import (
    CommentEvent,
)


def test_comment_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = CommentEvent(
        id="comment-1",
        text="Nice live!",
        comment_type="LIVE",
        commented_on="https://instagram.com/p/abc",
        user="jane",
    )

    assert model.id == "comment-1"
    assert model.text == "Nice live!"
    assert model.comment_type == "LIVE"
    assert model.commented_on == "https://instagram.com/p/abc"
    assert model.user == "jane"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump["id"] == "comment-1"
    assert alias_dump["text"] == "Nice live!"
    assert alias_dump["comment_type"] == "LIVE"
    assert alias_dump["commented_on"] == "https://instagram.com/p/abc"
    assert alias_dump["user"] == "jane"


def test_comment_event_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = CommentEvent(text="Hi")

    assert model.id is None
    assert model.comment_type is None
    assert model.commented_on is None
    assert model.user is None


def test_comment_event_expects_validation_error_for_missing_required():
    """Test that text is required."""
    with pytest.raises(ValidationError):
        CommentEvent()
