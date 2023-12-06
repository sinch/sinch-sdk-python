from sinch.core.models.http_response import HTTPResponse
from sinch.domains.verification.endpoints.verification_endpoint import VerificationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
# from sinch.domains.conversation.models.contact.responses import CreateConversationContactResponse
# from sinch.domains.conversation.models.contact.requests import CreateConversationContactRequest


class StartVerificationEndpoint(VerificationEndpoint):
    ENDPOINT_URL = "{origin}/verification/v1/verifications"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.SIGNED.value

    def __init__(self, request_data):
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.verification_origin,
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse):
        pass
