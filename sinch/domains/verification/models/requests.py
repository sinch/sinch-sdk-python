from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.verification.enums import VerificationMethod


@dataclass
class StartVerificationRequest(SinchRequestBaseModel):
    identity: dict
    method: VerificationMethod
    reference: str
    custom: str
    flash_call_options: dict


@dataclass
class ReportVerificationUsingIdentityRequest(SinchRequestBaseModel):
    endpoint: str
    verification_report_request: dict


@dataclass
class ReportVerificationUsingIdRequest(SinchRequestBaseModel):
    id: str
    verification_report_request: dict


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
