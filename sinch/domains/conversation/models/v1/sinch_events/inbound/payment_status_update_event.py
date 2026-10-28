from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent
from sinch.domains.conversation.models.v1.sinch_events.inbound.payment_status_type import (
    PaymentStatusType,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.payment_transaction_status_type import (
    PaymentTransactionStatusType,
)


class PaymentStatusUpdateEvent(SinchEvent):
    """Message specific only for Payments feature to reflect current state of particular Payment Flow."""

    reference_id: Optional[StrictStr] = Field(
        default=None,
        description="This is the partner supplied ID to identify the order for payments",
    )
    payment_status: Optional[PaymentStatusType] = Field(
        default=None, description="Status reflecting how payment flow goes"
    )
    payment_transaction_status: Optional[PaymentTransactionStatusType] = Field(
        default=None,
        description="Group of statuses of the user-initiated transaction changes.",
    )
    payment_transaction_id: Optional[StrictStr] = Field(
        default=None,
        description="Unique id of the transaction for which one of the transaction payment_transaction_status is present in event.",
    )
