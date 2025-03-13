from sinch.core.models.http_response import HTTPResponse
from sinch.domains.numbers.api.v1.internal.numbers_endpoint import NumbersEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.numbers.models.callbacks.responses import GetNumbersCallbackConfigurationResponse


class GetNumbersCallbackConfigurationEndpoint(NumbersEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/callbackConfiguration"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str):
        super().__init__(project_id, None)
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id
        )

    def handle_response(self, response: HTTPResponse) -> GetNumbersCallbackConfigurationResponse:
        super().handle_response(response)
        return GetNumbersCallbackConfigurationResponse(
            project_id=response.body['projectId'],
            hmac_secret=response.body['hmacSecret']
        )
