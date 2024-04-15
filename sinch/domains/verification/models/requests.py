from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.verification.enums import VerificationMethod


@dataclass
class StartVerificationRequest(SinchRequestBaseModel):
    identity: dict
    reference: str
    custom: str



@dataclass
class StartSMSVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.SMS.value


@dataclass
class StartFlashCallVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.FLASHCALL.value


@dataclass
class StartCalloutVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.CALLOUT.value


@dataclass
class StartSeamlessVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.SEAMLESS.value


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
    method: VerificationMethod
