from sinch.domains.verification.endpoints.start_verification import StartVerificationEndpoint
from sinch.domains.verification.endpoints.report_verification_using_identity import (
    ReportVerificationUsingIdentityEndpoint
)
from sinch.domains.verification.endpoints.report_verification_with_id import (
    ReportVerificationWithIdEndpoint
)
from sinch.domains.verification.endpoints.get_verification_by_id import (
    GetVerificationByIdEndpoint
)
from sinch.domains.verification.endpoints.get_verification_by_identity import (
    GetVerificationByIdentityEndpoint
)
from sinch.domains.verification.endpoints.get_verification_by_reference import (
    GetVerificationByReferenceEndpoint
)
from sinch.domains.verification.models.responses import (
    StartVerificationResponse,
    ReportVerificationUsingIdentityResponse,
    ReportVerificationWithIdResponse,
)
from sinch.domains.verification.models.requests import (
    StartVerificationRequest,
    ReportVerificationUsingIdentityRequest,
    ReportVerificationWithIdRequest,
)


class Verification:
    """
    Documentation for the Verification API: https://developers.sinch.com/docs/verification
    """
    def __init__(self, sinch):
        self._sinch = sinch

    def start(
        self,
        identity: dict,
        method: str,
        reference: str = None,
        custom: str = None,
        flash_call_options: object = None
    ) -> StartVerificationResponse:
        return self._sinch.configuration.transport.request(
            StartVerificationEndpoint(
                request_data=StartVerificationRequest(
                    identity=identity,
                    method=method,
                    reference=reference,
                    custom=custom,
                    flash_call_options=flash_call_options
                )
            )
        )

    def report_using_id(
        self,
        endpoint,
        method,
        sms_code=None,
        flash_call_cli=None,
        callout=None
    ) -> ReportVerificationUsingIdentityResponse:
        return self._sinch.configuration.transport.request(
            ReportVerificationUsingIdentityEndpoint(
                request_data=ReportVerificationUsingIdentityRequest(
                    endpoint,
                    method,
                    sms_code,
                    flash_call_cli,
                    callout
                )
            )
        )

    def report_using_identity(
        self,
        endpoint,
        method,
        sms_code=None,
        flash_call_cli=None,
        callout=None
    ) -> ReportVerificationUsingIdentityResponse:
        return self._sinch.configuration.transport.request(
            ReportVerificationUsingIdentityEndpoint(
                request_data=ReportVerificationUsingIdentityRequest(
                    endpoint,
                    method,
                    sms_code,
                    flash_call_cli,
                    callout
                )
            )
        )

    def get_by_reference(self, reference):
        return self._sinch.configuration.transport.request(
            ReportVerificationUsingIdentityEndpoint(
                request_data=ReportVerificationUsingIdentityResponse(
                    endpoint,
                    method,
                    sms_code,
                    flash_call_cli,
                    callout
                )
            )
        )

    def get_by_id(self, id):
        return self._sinch.configuration.transport.request(
            ReportVerificationUsingIdentityEndpoint(
                request_data=ReportVerificationUsingIdentityResponse(
                    endpoint,
                    method,
                    sms_code,
                    flash_call_cli,
                    callout
                )
            )
        )

    def get_by_identity(self, id):
        return self._sinch.configuration.transport.request(
            ReportVerificationUsingIdentityEndpoint(
                request_data=ReportVerificationUsingIdentityResponse(
                    endpoint,
                    method,
                    sms_code,
                    flash_call_cli,
                    callout
                )
            )
        )

