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
class ReportVerificationByIdentityRequest(SinchRequestBaseModel):
    endpoint: str
    verification_report_request: dict


@dataclass
class ReportVerificationByIdRequest(SinchRequestBaseModel):
    id: str
    verification_report_request: dict


@dataclass
class GetVerificationStatusByReferenceRequest(SinchRequestBaseModel):
    reference: str


@dataclass
class GetVerificationStatusByIdRequest(SinchRequestBaseModel):
    id: str


@dataclass
class GetVerificationStatusByIdentityRequest(SinchRequestBaseModel):
    endpoint: str
    method: str
