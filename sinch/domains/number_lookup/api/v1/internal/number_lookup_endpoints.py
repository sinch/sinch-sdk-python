import json
from typing import Type
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.core.types import BM
from sinch.domains.number_lookup.api.v1.internal.base import LookupEndpoint
from sinch.domains.number_lookup.exceptions import NumberLookupException
from sinch.domains.number_lookup.models.v1.internal import LookupNumberRequest
from sinch.domains.number_lookup.models.v1.response import LookupNumberResponse


class LookupNumberEndpoint(LookupEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/lookups"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: LookupNumberRequest):
        super(LookupNumberEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.number_lookup_origin,
            project_id=self.project_id,
        )

    def request_body(self) -> str:
        request_data = self.request_data.model_dump(
            by_alias=True, exclude_none=True
        )
        return json.dumps(request_data)

    def process_response_model(
        self, response_body: dict, response_model: Type[BM]
    ) -> BM:
        try:
            return response_model.model_validate(response_body)
        except Exception as e:
            raise ValueError(f"Invalid response structure: {e}") from e

    def handle_response(self, response: HTTPResponse) -> LookupNumberResponse:
        try:
            super(LookupNumberEndpoint, self).handle_response(response)
        except NumberLookupException as e:
            raise NumberLookupException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, LookupNumberResponse)
