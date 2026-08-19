"""Backwards-compatible re-export.

.. deprecated:: 2.2
    Import from ``sinch.domains.conversation.models.v1.shared.channel_identity``
    instead. This module is removed in 3.0.
"""

from sinch.domains.conversation.models.v1.shared.channel_identity import (
    ChannelIdentity,
)

__all__ = [
    "ChannelIdentity",
]
