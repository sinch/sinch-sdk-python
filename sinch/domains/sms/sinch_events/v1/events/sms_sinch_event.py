from typing import Union

from sinch.domains.sms.models.v1.response import (
    BatchDeliveryReport,
    RecipientDeliveryReport,
)
from sinch.domains.sms.models.v1.types.inbound_message import InboundMessage

IncomingSMSSinchEvent = InboundMessage

SmsSinchEventPayload = Union[
    InboundMessage,
    BatchDeliveryReport,
    RecipientDeliveryReport,
]
