from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class BatchRequest(SinchRequestBaseModel):
    def as_dict(self):
        payload = super(BatchRequest, self).as_dict()
        payload["to"] = payload.pop("to")
        if payload.get("from_"):
            payload["from"] = payload.pop("from_")
        return payload


@dataclass
class SendBatchRequest(BatchRequest):
    to: list
    from_: str
    body: str
    delivery_report: str
    parameters: dict
    send_at: str
    expire_at: str
    callback_url: str
    client_reference: str
    feedback_enabled: bool
    flash_message: bool
    truncate_concat: bool
    type_: str
    max_number_of_message_parts: int
    from_ton: int
    from_npi: int


@dataclass
class ListBatchesRequest(SinchRequestBaseModel):
    page_size: int
    from_s: str
    start_date: str
    end_date: str
    client_reference: str
    page: int = 0


@dataclass
class GetBatchRequest(SinchRequestBaseModel):
    batch_id: str


@dataclass
class CancelBatchRequest(SinchRequestBaseModel):
    batch_id: str


@dataclass
class BatchDryRunRequest(BatchRequest):
    per_recipient: bool
    number_of_recipients: int
    to: str
    from_: str
    body: str
    type_: str
    udh: str
    delivery_report: str
    parameters: dict
    send_at: str
    expire_at: str
    callback_url: str
    client_reference: str
    flash_message: bool
    max_number_of_message_parts: int


@dataclass
class UpdateBatchRequest(SinchRequestBaseModel):
    batch_id: str
    to_add: list
    to_remove: list
    from_: str
    body: str
    delivery_report: str
    send_at: str
    expire_at: str
    callback_url: str


@dataclass
class ReplaceBatchRequest(BatchRequest):
    batch_id: str
    to: str
    from_: str
    body: str
    delivery_report: str
    parameters: dict
    send_at: str
    expire_at: str
    type_: str
    callback_url: str
    client_reference: str
    flash_message: bool
    max_number_of_message_parts: int
    udh: str


@dataclass
class SendDeliveryFeedbackRequest(SinchRequestBaseModel):
    batch_id: str
    recipients: list
