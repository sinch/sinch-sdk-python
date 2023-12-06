from sinch.domains.verification.endpoints.start_verification import StartVerificationEndpoint
from sinch.domains.verification.models.responses import StartVerificationResponse
from sinch.domains.verification.models.requests import StartVerificationRequest


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

    def get_by_id(self):
        pass

    def get_by_identity(self):
        pass

    def get_by_reference(self):
        pass

    def report_using_id(self):
        pass

    def report_using_identity(self):
        pass
