from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class ListSMSDeliveryReportsResponse(SinchBaseModel):
    page: str
    page_size: str
    count: str
    delivery_reports: list


@dataclass
class GetSMSDeliveryReportForBatchResponse(SinchBaseModel):
    type: str
    batch_id: str
    total_message_count: str
    statuses: list
    client_reference: str


@dataclass
class GetSMSDeliveryReportForNumberResponse(SinchBaseModel):
    at: str
    batch_id: str
    code: int
    recipient: str
    status: str
    applied_originator: str
    client_reference: str
    number_of_message_parts: str
    operator: str
    operator_status_at: str
    type: str
