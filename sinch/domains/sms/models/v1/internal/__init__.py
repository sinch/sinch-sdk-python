from sinch.domains.sms.models.v1.internal.batch_id_request import (
    BatchIdRequest,
)
from sinch.domains.sms.models.v1.internal.delivery_feedback_request import (
    DeliveryFeedbackRequest,
)
from sinch.domains.sms.models.v1.internal.list_batches_request import (
    ListBatchesRequest,
)
from sinch.domains.sms.models.v1.internal.list_delivery_reports_response import (
    ListDeliveryReportsResponse,
)
from sinch.domains.sms.models.v1.internal.get_recipient_delivery_report_request import (
    GetRecipientDeliveryReportRequest,
)
from sinch.domains.sms.models.v1.internal.get_batch_delivery_report_request import (
    GetBatchDeliveryReportRequest,
)
from sinch.domains.sms.models.v1.internal.list_delivery_reports_request import (
    ListDeliveryReportsRequest,
)

__all__ = [
    "BatchIdRequest",
    "DeliveryFeedbackRequest",
    "ListBatchesRequest",
    "ListDeliveryReportsResponse",
    "GetRecipientDeliveryReportRequest",
    "ListDeliveryReportsRequest",
    "GetBatchDeliveryReportRequest",
    "DryRunRequest",
    "ReplaceBatchRequest",
    "SendSMSRequest",
    "UpdateBatchMessageRequest",
]


# Lazy import to avoid circular dependency
def __getattr__(name: str):
    if name == "DryRunRequest":
        from sinch.domains.sms.models.v1.internal.dry_run_request import (
            DryRunRequest,
        )

        return DryRunRequest
    if name == "ReplaceBatchRequest":
        from sinch.domains.sms.models.v1.internal.replace_batch_request import (
            ReplaceBatchRequest,
        )

        return ReplaceBatchRequest
    if name == "SendSMSRequest":
        from sinch.domains.sms.models.v1.internal.send_sms_request import (
            SendSMSRequest,
        )

        return SendSMSRequest
    if name == "UpdateBatchMessageRequest":
        from sinch.domains.sms.models.v1.internal.update_batch_message_request import (
            UpdateBatchMessageRequest,
        )

        return UpdateBatchMessageRequest
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
