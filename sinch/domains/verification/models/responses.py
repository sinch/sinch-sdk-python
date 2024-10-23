from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.verification.enums import VerificationMethod, VerificationStatus


@dataclass
class FlashCallResponse:
    cli_filter: str
    interception_timeout: int
    report_timeout: int
    deny_call_after: int


@dataclass
class SMSResponse:
    template: str
    interception_timeout: str


@dataclass
class DataResponse:
    target_uri: str


@dataclass
class StartVerificationResponse(SinchBaseModel):
    id: str
    method: VerificationMethod
    _links: list


@dataclass
class StartFlashCallInitiateVerificationResponse(StartVerificationResponse):
    flash_call: FlashCallResponse


@dataclass
class StartDataInitiateVerificationResponse(StartVerificationResponse):
    seamless: DataResponse


@dataclass
class StartCalloutInitiateVerificationResponse(StartVerificationResponse):
    pass


@dataclass
class StartSMSVerificationResponse(StartVerificationResponse):
    sms: SMSResponse


@dataclass
class StartFlashCallVerificationResponse(StartVerificationResponse):
    flash_call: FlashCallResponse


@dataclass
class StartDataVerificationResponse(StartVerificationResponse):
    seamless: DataResponse


@dataclass
class StartPhoneCallVerificationResponse(StartVerificationResponse):
    pass


@dataclass
class VerificationResponse(SinchBaseModel):
    id: str
    method: VerificationMethod
    status: VerificationStatus
    price: dict
    identity: dict
    country_id: str
    verification_timestamp: str
    reference: str
    reason: str
    call_complete: bool


@dataclass
class GetVerificationStatusByIdResponse(VerificationResponse):
    pass


@dataclass
class ReportVerificationResponse(VerificationResponse):
    pass


@dataclass
class ReportVerificationByIdentityResponse(ReportVerificationResponse):
    pass


@dataclass
class ReportVerificationByIdResponse(ReportVerificationResponse):
    pass


@dataclass
class GetVerificationStatusByReferenceResponse(VerificationResponse):
    pass


@dataclass
class GetVerificationStatusByIdentityResponse(VerificationResponse):
    pass
