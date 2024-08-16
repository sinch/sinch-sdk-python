from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.verification.enums import VerificationMethod
from sinch.domains.verification.models import VerificationIdentity


class ReporPhoneCallVerificationDataTransfromationMixin:
    def as_dict(self):
        request_data = super().as_dict()
        payload = {"method": request_data["method"], "callout": {}}

        if request_data.get("code"):
            payload["callout"]["code"] = request_data["code"]

        return payload


class ReporFlashCallVerificationDataTransfromationMixin:
    def as_dict(self):
        request_data = super().as_dict()
        payload = {"method": request_data["method"], "flashCall": {}}

        if request_data.get("cli"):
            payload["flashCall"]["cli"] = request_data["cli"]

        return payload


class ReporSMSVerificationDataTransfromationMixin:
    def as_dict(self):
        request_data = super().as_dict()
        payload = {"method": request_data["method"], "sms": {}}

        if request_data.get("code"):
            payload["sms"]["code"] = request_data["code"]

        if request_data.get("cli"):
            payload["sms"]["cli"] = request_data["cli"]

        return payload


@dataclass
class StartVerificationRequest(SinchRequestBaseModel):
    identity: VerificationIdentity
    reference: str
    custom: str


@dataclass
class StartSMSVerificationRequest(StartVerificationRequest):
    expiry: str
    code_type: str
    template: str
    method: str = VerificationMethod.SMS.value

    def as_dict(self):
        payload = super().as_dict()
        payload["smsOptions"] = {}

        if payload.get("code_type"):
            payload["smsOptions"].update({
                "codeType": payload.pop("code_type")
            })
        elif payload.get("expiry"):
            payload["smsOptions"].update({
                "expiry": payload.pop("expiry")
            })
        elif payload.get("template"):
            payload["smsOptions"].update({
                "template": payload.pop("template")
            })
        return payload


@dataclass
class StartFlashCallVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.FLASH_CALL.value


@dataclass
class StartPhoneCallVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.CALLOUT.value


@dataclass
class StartDataVerificationRequest(StartVerificationRequest):
    method: str = VerificationMethod.SEAMLESS.value


@dataclass
class ReportVerificationByIdentityRequest(SinchRequestBaseModel):
    endpoint: str


@dataclass
class ReportVerificationByIdentityAndSMSRequest(
    ReporSMSVerificationDataTransfromationMixin,
    ReportVerificationByIdentityRequest
):
    code: str
    cli: str
    method: str = VerificationMethod.SMS.value


@dataclass
class ReportVerificationByIdentityAndFlashCallRequest(
    ReporFlashCallVerificationDataTransfromationMixin,
    ReportVerificationByIdentityRequest
):
    cli: str
    method: str = VerificationMethod.FLASH_CALL.value


@dataclass
class ReportVerificationByIdentityAndPhoneCallRequest(
    ReporPhoneCallVerificationDataTransfromationMixin,
    ReportVerificationByIdentityRequest
):
    code: str
    method: str = VerificationMethod.CALLOUT.value


@dataclass
class ReportVerificationByIdRequest(SinchRequestBaseModel):
    id: str


@dataclass
class ReportVerificationByIdAndSMSRequest(
    ReporSMSVerificationDataTransfromationMixin,
    ReportVerificationByIdRequest
):
    code: str
    cli: str
    method: str = VerificationMethod.SMS.value


@dataclass
class ReportVerificationByIdAndFlashCallRequest(
    ReporFlashCallVerificationDataTransfromationMixin,
    ReportVerificationByIdRequest
):
    cli: str
    method: str = VerificationMethod.FLASH_CALL.value


@dataclass
class ReportVerificationByIdAndPhoneCallRequest(
    ReporPhoneCallVerificationDataTransfromationMixin,
    ReportVerificationByIdRequest
):
    code: str
    method: str = VerificationMethod.CALLOUT.value


@dataclass
class GetVerificationStatusByReferenceRequest(SinchRequestBaseModel):
    reference: str


@dataclass
class GetVerificationStatusByIdentityRequest(SinchRequestBaseModel):
    endpoint: str
    method: str
