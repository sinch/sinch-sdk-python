from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class ListSMSDeliveryReportsRequest(SinchRequestBaseModel):
    code: str
    status: str
    start_date: str
    end_date: str
    client_reference: str
    page_size: int
    page: int = 0


@dataclass
class GetSMSDeliveryReportForBatchRequest(SinchRequestBaseModel):
    batch_id: str
    type_: str
    status: list
    code: list


@dataclass
class GetSMSDeliveryReportForNumberRequest(SinchRequestBaseModel):
    batch_id: str
    recipient_number: str
