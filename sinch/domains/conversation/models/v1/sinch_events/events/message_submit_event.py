"""Backwards-compatible re-export.

.. deprecated:: 2.4
    Import from ``sinch.domains.conversation.models.v1.sinch_events.message.message_submit_event``
    (or from ``sinch.domains.conversation.models.v1.sinch_events``) instead. This module is removed in 3.0.
"""

from sinch.domains.conversation.models.v1.sinch_events.message.message_submit_event import (
    MessageSubmitEvent,
)

__all__ = [
    "MessageSubmitEvent",
]
