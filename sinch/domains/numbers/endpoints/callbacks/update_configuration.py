from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.internal.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.numbers.models.callbacks.responses import UpdateNumbersCallbackConfigurationResponse
from sinch.domains.numbers.models.callbacks.requests import UpdateNumbersCallbackConfigurationRequest


class UpdateNumbersCallbackConfigurationEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/callbackConfiguration"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: UpdateNumbersCallbackConfigurationRequest):
        super().__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id
        )

    def request_body(self):
        return self.request_data.as_json()

    def handle_response(self, response: HTTPResponse) -> UpdateNumbersCallbackConfigurationResponse:
        super().handle_response(response)
        return UpdateNumbersCallbackConfigurationResponse(
            project_id=response.body['projectId'],
            hmac_secret=response.body['hmacSecret']
        )
