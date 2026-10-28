"""Backwards-compatible re-export.

.. deprecated:: 2.4
    Import from ``sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base``
    (or from ``sinch.domains.conversation.models.v1.sinch_events``) instead. This module is removed in 3.0.
"""

from sinch.domains.conversation.models.v1.sinch_events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)

__all__ = [
    "ConversationSinchEventBase",
]
