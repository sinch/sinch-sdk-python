from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class StartVerificationRequest(SinchRequestBaseModel):
    identity: dict
    method: str
    reference: str
    custom: str
    flash_call_options: object


@dataclass
class ReportVerificationUsingIdentityRequest(SinchRequestBaseModel):
    endpoint: str
    method: str
    sms_code: str
    flash_call_cli: str
    callout: str


@dataclass
class ReportVerificationUsingIdRequest(SinchRequestBaseModel):
    pass


@dataclass
class GetVerificationByReferenceRequest(SinchRequestBaseModel):
    reference: str


@dataclass
class GetVerificationByIdRequest(SinchRequestBaseModel):
    id: str


@dataclass
class GetVerificationByIdentityRequest(SinchRequestBaseModel):
    endpoint: str
    method: str
