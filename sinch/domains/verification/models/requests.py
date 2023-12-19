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
    pass


@dataclass
class GetVerificationByIdRequest(SinchRequestBaseModel):
    pass


@dataclass
class GetVerificationByIdentityRequest(SinchRequestBaseModel):
    pass
