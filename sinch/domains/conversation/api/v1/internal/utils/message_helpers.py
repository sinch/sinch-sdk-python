"""
Helper functions for building and processing message requests.

This module contains pure utility functions that handle common operations
for message sending, such as recipient validation, type coercion, and
parameter splitting.
"""

from typing import List, Optional, Union

from sinch.domains.conversation.models.v1.messages.internal.request.recipient import (
    ChannelRecipientIdentity,
    IdentifiedBy,
    Recipient,
)
from sinch.domains.conversation.models.v1.messages.internal.request.send_message_request_body import (
    SendMessageRequestBody,
)
from sinch.domains.conversation.models.v1.messages.types import (
    ChannelRecipientIdentityDict,
    RecipientDict,
)


def build_recipient_dict(
    contact_id: Optional[str] = None,
    recipient_identities: Optional[List[ChannelRecipientIdentityDict]] = None,
) -> RecipientDict:
    """
    Build a RecipientDict from optional contact_id or recipient_identities.

    Validates that exactly one of the parameters is provided and returns
    the appropriate dictionary structure.

    :param contact_id: The contact ID of the recipient.
    :type contact_id: Optional[str]
    :param recipient_identities: List of channel identities for the recipient.
    :type recipient_identities: Optional[List[ChannelRecipientIdentityDict]]

    :returns: A RecipientDict with either contact_id or channel_identities.
    :rtype: RecipientDict

    :raises ValueError: If both or neither parameters are provided.
    """
    has_contact_id = contact_id is not None
    has_identities = recipient_identities is not None

    if has_contact_id and has_identities:
        raise ValueError(
            "Cannot specify both 'contact_id' and 'recipient_identities'. "
            "Provide exactly one."
        )
    if not has_contact_id and not has_identities:
        raise ValueError(
            "Must provide either 'contact_id' or 'recipient_identities'."
        )

    return (
        {"contact_id": contact_id}
        if has_contact_id
        else {"channel_identities": recipient_identities}
    )


def coerce_recipient(recipient: Union[Recipient, dict]) -> Recipient:
    """
    Coerce a recipient input to a Recipient model instance.

    Handles multiple input formats:
    - Recipient model instance (returns as-is)
    - Simplified dict: {"channel_identities": [...]}
    - Simplified dict: {"contact_id": "..."}
    - Full form dict: {"identified_by": {"channel_identities": [...]}}

    :param recipient: The recipient as a Recipient model or dict.
    :type recipient: Union[Recipient, dict]

    :returns: A Recipient model instance.
    :rtype: Recipient
    """
    if isinstance(recipient, dict):
        # Allow passing recipient dict in simplified form:
        # - {"channel_identities": [...]} -> converts to {"identified_by": {"channel_identities": [...]}}
        # - {"contact_id": "..."}
        # - Or full form: {"identified_by": {"channel_identities": [...]}}
        if (
            "channel_identities" in recipient
            and "identified_by" not in recipient
        ):
            channel_identities = [
                ChannelRecipientIdentity(**ci) if isinstance(ci, dict) else ci
                for ci in recipient["channel_identities"]
            ]
            return Recipient(
                identified_by=IdentifiedBy(
                    channel_identities=channel_identities
                )
            )
        return Recipient(**recipient)
    return recipient


def split_send_kwargs(kwargs: dict) -> tuple[dict, dict]:
    """
    Split kwargs into message-level and request-level parameters.

    Separates keyword arguments into two groups:
    - message_kwargs: Fields that belong under the `message` field
    - request_kwargs: Fields that belong on the SendMessageRequest itself

    :param kwargs: Dictionary of keyword arguments to split.
    :type kwargs: dict

    :returns: A tuple of (message_kwargs, request_kwargs).
    :rtype: tuple[dict, dict]
    """
    message_fields = set(SendMessageRequestBody.model_fields.keys())
    message_kwargs = {k: v for k, v in kwargs.items() if k in message_fields}
    request_kwargs = {
        k: v for k, v in kwargs.items() if k not in message_fields
    }
    return message_kwargs, request_kwargs
