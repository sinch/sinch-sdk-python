from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.verification.enums import VerificationMethod
from sinch.domains.verification.models import VerificationIdentity


@dataclass
class StartVerificationRequest(SinchRequestBaseModel):
    identity: VerificationIdentity
    reference: str
    custom: str


@dataclass
class StartSMSVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.SMS.value
    expiry: str = None
    code_type: str = None
    template: str = None


@dataclass
class StartFlashCallVerificationRequest(StartVerificationRequest):
    dial_timeout: int
    method: str = VerificationMethod.FLASHCALL.value


@dataclass
class StartCalloutVerificationRequest(StartVerificationRequest):
    speech_locale: str
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
