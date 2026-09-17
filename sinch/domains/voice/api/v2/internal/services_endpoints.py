from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.api.v2.internal.base.voice_endpoint import (
    VoiceEndpoint,
)
from sinch.domains.voice.models.v2.services.internal.list_services_response import (
    ListServicesResponse,
)
from sinch.domains.voice.models.v2.services.internal.request.create_service_request import (
    CreateServiceRequest,
)
from sinch.domains.voice.models.v2.services.internal.request.list_services_request import (
    ListServicesRequest,
)
from sinch.domains.voice.models.v2.services.internal.request.service_id_request import (
    ServiceIdRequest,
)
from sinch.domains.voice.models.v2.services.internal.request.update_service_request import (
    UpdateServiceRequest,
)
from sinch.domains.voice.models.v2.services.response.service_response import (
    ServiceResponse,
)


class ListServicesEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/services"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {"filter", "is_default", "page_size", "page"}

    def __init__(
        self,
        project_id: str,
        request_data: ListServicesRequest,
        response_model=ListServicesResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class CreateServiceEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/services"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    HEADER_PARAM_FIELDS = {"idempotency_key"}

    def __init__(
        self,
        project_id: str,
        request_data: CreateServiceRequest,
        response_model=ServiceResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class GetServiceEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/services/{service_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ServiceIdRequest,
        response_model=ServiceResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class UpdateServiceEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/services/{service_id}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    HEADER_PARAM_FIELDS = {"idempotency_key"}

    def __init__(
        self,
        project_id: str,
        request_data: UpdateServiceRequest,
        response_model=ServiceResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class DeleteServiceEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/services/{service_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ServiceIdRequest):
        super().__init__(project_id, request_data)
