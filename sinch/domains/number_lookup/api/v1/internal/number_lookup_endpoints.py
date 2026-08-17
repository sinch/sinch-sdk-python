from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.number_lookup.api.v1.internal.base import LookupEndpoint
from sinch.domains.number_lookup.models.v1.internal import LookupNumberRequest
from sinch.domains.number_lookup.models.v1.response import LookupNumberResponse


class LookupNumberEndpoint(LookupEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/lookups"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: LookupNumberRequest,
        response_model=LookupNumberResponse,
    ):
        super().__init__(project_id, request_data, response_model)
