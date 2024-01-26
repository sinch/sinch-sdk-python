from sinch.domains.verification.endpoints.start_verification import StartVerificationEndpoint
from sinch.domains.verification.endpoints.report_verification_using_identity import (
    ReportVerificationByIdentityEndpoint
)
from sinch.domains.verification.endpoints.report_verification_using_id import (
    ReportVerificationByIdEndpoint
)
from sinch.domains.verification.endpoints.get_verification_by_id import (
    GetVerificationStatusByIdEndpoint
)
from sinch.domains.verification.endpoints.get_verification_by_identity import (
    GetVerificationStatusByIdentityEndpoint
)
from sinch.domains.verification.endpoints.get_verification_by_reference import (
    GetVerificationStatusByReferenceEndpoint
)
from sinch.domains.verification.models.responses import (
    StartVerificationResponse,
    ReportVerificationByIdentityResponse,
    ReportVerificationByIdResponse,
    GetVerificationStatusByIdentityResponse,
    GetVerificationStatusByIdResponse,
    GetVerificationStatusByReferenceResponse
)
from sinch.domains.verification.models.requests import (
    StartVerificationRequest,
    ReportVerificationByIdentityRequest,
    ReportVerificationByIdRequest,
    GetVerificationStatusByIdRequest,
    GetVerificationStatusByIdentityRequest,
    GetVerificationStatusByReferenceRequest
)

from sinch.domains.verification.enums import VerificationMethod


class Verifications:
    def __init__(self, sinch):
        self._sinch = sinch

    def start(
        self,
        identity: dict,
        method: VerificationMethod,
        reference: str = None,
        custom: str = None,
        flash_call_options: dict = None
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

    def report_by_id(
        self,
        id: str,
        verification_report_request: dict
    ) -> ReportVerificationByIdResponse:
        return self._sinch.configuration.transport.request(
            ReportVerificationByIdEndpoint(
                request_data=ReportVerificationByIdRequest(
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
        return self._sinch.configuration.transport.request(
            ReportVerificationByIdentityEndpoint(
                request_data=ReportVerificationByIdentityRequest(
                    endpoint,
                    verification_report_request
                )
            )
        )


class VerificationStatus:
    def __init__(self, sinch):
        self._sinch = sinch

    def get_by_reference(self, reference) -> GetVerificationStatusByReferenceResponse:
        return self._sinch.configuration.transport.request(
            GetVerificationStatusByReferenceEndpoint(
                request_data=GetVerificationStatusByReferenceRequest(
                    reference=reference
                )
            )
        )

    def get_by_id(self, id) -> GetVerificationStatusByIdResponse:
        return self._sinch.configuration.transport.request(
            GetVerificationStatusByIdEndpoint(
                request_data=GetVerificationStatusByIdRequest(
                    id=id
                )
            )
        )

    def get_by_identity(self, endpoint, method) -> GetVerificationStatusByIdentityResponse:
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


class VerificationAsync(VerificationBase):
    """
    Asynchronous version of the Verification Domain
    """
    __doc__ += VerificationBase.__doc__

    def __init__(self, sinch):
        super(VerificationAsync, self).__init__(sinch)
        self.verifications = Verifications(self._sinch)
        self.verification_status = VerificationStatus(self._sinch)
