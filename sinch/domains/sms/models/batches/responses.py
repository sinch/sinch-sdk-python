from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.sms.models.batches import Batch


@dataclass
class SendSMSBatchResponse(Batch):
    pass


@dataclass
class ReplaceSMSBatchResponse(Batch):
    pass


@dataclass
class ListSMSBatchesResponse(SinchBaseModel):
    page: str
    page_size: str
    count: str
    batches: list


@dataclass
class GetSMSBatchResponse(Batch):
    pass


@dataclass
class CancelSMSBatchResponse(Batch):
    pass


@dataclass
class SendSMSBatchDryRunResponse(SinchBaseModel):
    number_of_recipients: int
    number_of_messages: int
    per_recipient: list


@dataclass
class UpdateSMSBatchResponse(SinchBaseModel):
    id: str
    to: list
    from_: str
    body: str
    campaign_id: str
    delivery_report: str
    send_at: str
    expire_at: str
    callback_url: str
    cancelled: bool
    type: str
    created_at: str
    modified_at: str


@dataclass
class SendSMSDeliveryFeedbackResponse(SinchBaseModel):
    pass
