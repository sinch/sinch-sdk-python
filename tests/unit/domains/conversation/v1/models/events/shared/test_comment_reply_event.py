import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.events.shared.comment_reply_event import (
    CommentReplyEvent,
)


def test_comment_reply_event_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = CommentReplyEvent(text="Thanks for your comment!")

    assert model.text == "Thanks for your comment!"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert alias_dump == {"text": "Thanks for your comment!"}


def test_comment_reply_event_expects_validation_error_for_missing_required():
    """Test that text is required."""
    with pytest.raises(ValidationError):
        CommentReplyEvent()


def test_comment_reply_event_expects_validation_error_for_non_string_text():
    """Test that text must be a string."""
    with pytest.raises(ValidationError):
        CommentReplyEvent(text=123)
