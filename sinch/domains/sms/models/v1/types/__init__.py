from sinch.domains.sms.models.v1.types.delivery_receipt_status_code_type import (
    DeliveryReceiptStatusCodeType,
)
from sinch.domains.sms.models.v1.types.delivery_report_type import (
    DeliveryReportType,
)
from sinch.domains.sms.models.v1.types.delivery_status_type import (
    DeliveryStatusType,
)
from sinch.domains.sms.models.v1.types.encoding_type import EncodingType
from sinch.domains.sms.models.v1.types.recipient_delivery_report_type import (
    RecipientDeliveryReportType,
)

__all__ = [
    "BatchResponse",
    "DeliveryReceiptStatusCodeType",
    "DeliveryReportType",
    "DeliveryStatusType",
    "EncodingType",
    "RecipientDeliveryReportType",
]


# Lazy import to avoid circular dependency
# BatchResponse imports from shared which may import from types
def __getattr__(name: str):
    if name == "BatchResponse":
        from sinch.domains.sms.models.v1.types.batch_response import (
            BatchResponse,
        )

        return BatchResponse
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
