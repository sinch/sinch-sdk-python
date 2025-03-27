from sinch.domains.verification.endpoints.start_verification import StartVerificationEndpoint
from sinch.domains.verification.endpoints.report_verification_using_identity import (
    ReportVerificationByIdentityEndpoint
)
from sinch.domains.verification.endpoints.report_verification_using_id import (
    ReportVerificationByIdEndpoint
)
from sinch.domains.verification.endpoints.get_verification_by_identity import (
    GetVerificationStatusByIdentityEndpoint
)
from sinch.domains.verification.endpoints.get_verification_by_reference import (
    GetVerificationStatusByReferenceEndpoint
)
from sinch.domains.verification.endpoints.get_verification_by_id import (
    GetVerificationStatusByIdEndpoint
)
from sinch.domains.verification.models.responses import (
    StartVerificationResponse,
    ReportVerificationByIdentityResponse,
    ReportVerificationByIdResponse,
    GetVerificationStatusByIdentityResponse,
    GetVerificationStatusByReferenceResponse,
    GetVerificationStatusByIdResponse
)
from sinch.domains.verification.models.requests import (
    StartSMSVerificationRequest,
    StartFlashCallVerificationRequest,
    StartPhoneCallVerificationRequest,
    StartCalloutVerificationRequest,
    StartDataVerificationRequest,
    ReportVerificationByIdentityRequestLegacy,
    ReportVerificationByIdRequestLegacy,
    ReportVerificationByIdentityAndSMSRequest,
    ReportVerificationByIdentityAndFlashCallRequest,
    ReportVerificationByIdentityAndPhoneCallRequest,
    ReportVerificationByIdAndSMSRequest,
    ReportVerificationByIdAndFlashCallRequest,
    ReportVerificationByIdAndPhoneCallRequest,
    GetVerificationStatusByIdentityRequest,
    GetVerificationStatusByReferenceRequest,
    GetVerificationStatusByIdRequest
)
from sinch.domains.verification.models import VerificationIdentity


class Verifications:
    def __init__(self, sinch):
        self._sinch = sinch

    def start_sms(
        self,
        identity: VerificationIdentity,
        reference: str = None,
        custom: str = None,
        expiry: str = None,
        code_type: str = None,
        template: str = None
    ) -> StartVerificationResponse:
        return self._sinch.configuration.transport.request(
            StartVerificationEndpoint(
                request_data=StartSMSVerificationRequest(
                    identity=identity,
                    reference=reference,
                    custom=custom,
                    expiry=expiry,
                    code_type=code_type,
                    template=template
                )
            )
        )

    def start_flash_call(
        self,
        identity: VerificationIdentity,
        reference: str = None,
        dial_timeout: int = None,
        custom: str = None
    ) -> StartVerificationResponse:
        return self._sinch.configuration.transport.request(
            StartVerificationEndpoint(
                request_data=StartFlashCallVerificationRequest(
                    identity=identity,
                    reference=reference,
                    dial_timeout=dial_timeout,
                    custom=custom
                )
            )
        )

    def start_phone_call(
        self,
        identity: VerificationIdentity,
        reference: str = None,
        custom: str = None
    ) -> StartVerificationResponse:
        return self._sinch.configuration.transport.request(
            StartVerificationEndpoint(
                request_data=StartPhoneCallVerificationRequest(
                    identity=identity,
                    reference=reference,
                    custom=custom
                )
            )
        )

    def start_callout(
        self,
        identity: VerificationIdentity,
        reference: str = None,
        custom: str = None,
        speech_locale: str = None
    ) -> StartVerificationResponse:
        """
        This method is not supported anymore.
        It should be used only for backward compatibility reasons.
        Use start_phone_call method instead.
        """
        return self._sinch.configuration.transport.request(
            StartVerificationEndpoint(
                request_data=StartCalloutVerificationRequest(
                    identity=identity,
                    reference=reference,
                    custom=custom,
                    speech_locale=speech_locale
                )
            )
        )

    def start_seamless(
        self,
        identity: VerificationIdentity,
        reference: str = None,
        custom: str = None
    ) -> StartVerificationResponse:
        """
        This method is not supported anymore.
        It should be used only for backward compatibility reasons.
        Use start_data method instead.
        """
        return self._sinch.configuration.transport.request(
            StartVerificationEndpoint(
                request_data=StartDataVerificationRequest(
                    identity=identity,
                    reference=reference,
                    custom=custom
                )
            )
        )

    def start_data(
        self,
        identity: VerificationIdentity,
        reference: str = None,
        custom: str = None
    ) -> StartVerificationResponse:
        return self._sinch.configuration.transport.request(
            StartVerificationEndpoint(
                request_data=StartDataVerificationRequest(
                    identity=identity,
                    reference=reference,
                    custom=custom
                )
            )
        )

    def report_sms_by_id(
        self,
        id: str,
        code: str,
        cli: str = None
    ) -> ReportVerificationByIdResponse:
        return self._sinch.configuration.transport.request(
            ReportVerificationByIdEndpoint(
                request_data=ReportVerificationByIdAndSMSRequest(
                    id,
                    code,
                    cli
                )
            )
        )

    def report_flash_call_by_id(
        self,
        id: str,
        cli: str
    ) -> ReportVerificationByIdResponse:
        return self._sinch.configuration.transport.request(
            ReportVerificationByIdEndpoint(
                request_data=ReportVerificationByIdAndFlashCallRequest(
                    id,
                    cli
                )
            )
        )

    def report_phone_call_by_id(
        self,
        id: str,
        code: str = None
    ) -> ReportVerificationByIdResponse:
        return self._sinch.configuration.transport.request(
            ReportVerificationByIdEndpoint(
                request_data=ReportVerificationByIdAndPhoneCallRequest(
                    id,
                    code
                )
            )
        )

    def report_sms_by_identity(
        self,
        endpoint: str,
        code: str,
        cli: str = None
    ) -> ReportVerificationByIdentityResponse:
        return self._sinch.configuration.transport.request(
            ReportVerificationByIdentityEndpoint(
                request_data=ReportVerificationByIdentityAndSMSRequest(
                    endpoint,
                    code,
                    cli
                )
            )
        )

    def report_flash_call_by_identity(
        self,
        endpoint: str,
        cli: str = None
    ) -> ReportVerificationByIdentityResponse:
        return self._sinch.configuration.transport.request(
            ReportVerificationByIdentityEndpoint(
                request_data=ReportVerificationByIdentityAndFlashCallRequest(
                    endpoint,
                    cli
                )
            )
        )

    def report_phone_call_by_identity(
        self,
        endpoint: str,
        code: str
    ) -> ReportVerificationByIdentityResponse:
        return self._sinch.configuration.transport.request(
            ReportVerificationByIdentityEndpoint(
                request_data=ReportVerificationByIdentityAndPhoneCallRequest(
                    endpoint,
                    code
                )
            )
        )

    def report_by_id(
        self,
        id: str,
        verification_report_request: dict
    ) -> ReportVerificationByIdResponse:
        """
        This method is not supported anymore.
        It should be used only for backward compatibility reasons.
        """
        return self._sinch.configuration.transport.request(
            ReportVerificationByIdEndpoint(
                request_data=ReportVerificationByIdRequestLegacy(
                    id,
                    verification_report_request
                )
            )
        )

    def report_by_identity(
        self,
        endpoint,
        verification_report_request
    ) -> ReportVerificationByIdentityResponse:
        """
        This method is not supported anymore.
        It should be used only for backward compatibility reasons.
        """
        return self._sinch.configuration.transport.request(
            ReportVerificationByIdentityEndpoint(
                request_data=ReportVerificationByIdentityRequestLegacy(
                    endpoint,
                    verification_report_request
                )
            )
        )


class VerificationStatus:
    def __init__(self, sinch):
        self._sinch = sinch

    def get_by_id(self, id: str) -> GetVerificationStatusByIdResponse:
        return self._sinch.configuration.transport.request(
            GetVerificationStatusByIdEndpoint(
                request_data=GetVerificationStatusByIdRequest(
                    id=id
                )
            )
        )

    def get_by_reference(self, reference: str) -> GetVerificationStatusByReferenceResponse:
        return self._sinch.configuration.transport.request(
            GetVerificationStatusByReferenceEndpoint(
                request_data=GetVerificationStatusByReferenceRequest(
                    reference=reference
                )
            )
        )

    def get_by_identity(
        self,
        endpoint: str,
        method: str
    ) -> GetVerificationStatusByIdentityResponse:
        return self._sinch.configuration.transport.request(
            GetVerificationStatusByIdentityEndpoint(
                request_data=GetVerificationStatusByIdentityRequest(
                    endpoint=endpoint,
                    method=method
                )
            )
        )


class VerificationBase:
    """
    Documentation for the Verification API: https://developers.sinch.com/docs/verification/
    """
    def __init__(self, sinch):
        self._sinch = sinch


class Verification(VerificationBase):
    """
    Synchronous version of the Verification Domain
    """
    __doc__ += VerificationBase.__doc__

    def __init__(self, sinch):
        super(Verification, self).__init__(sinch)
        self.verifications = Verifications(self._sinch)
        self.verification_status = VerificationStatus(self._sinch)
