from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.capability.internal.lookup_capability_request import (
    LookupCapabilityRequest,
)
from sinch.domains.conversation.models.v1.capability.response.lookup_capability_response import (
    LookupCapabilityResponse,
)


class LookupCapabilityEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/capability:query"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: LookupCapabilityRequest,
        response_model=LookupCapabilityResponse,
    ):
        super().__init__(project_id, request_data, response_model)
