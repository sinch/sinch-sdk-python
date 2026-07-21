import json

from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.api.v1.exceptions import ConversationException
from sinch.domains.conversation.api.v1.internal.base.conversation_endpoint import (
    ConversationEndpoint,
)
from sinch.domains.conversation.models.v1.apps.internal.list_apps_request import (
    ListAppsRequest,
)
from sinch.domains.conversation.models.v1.apps.internal.list_apps_response import (
    ListAppsResponse,
)
from sinch.domains.conversation.models.v1.apps.request.create_app_request import (
    CreateAppRequest,
)
from sinch.domains.conversation.models.v1.apps.request.update_app_request import (
    UpdateAppRequest,
)
from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
)


class ListAppsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ListAppsRequest,
        response_model=ListAppsResponse,
    ):
        super(ListAppsEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data
        self.response_model = response_model

    def handle_response(self, response: HTTPResponse) -> ListAppsResponse:
        try:
            super(ListAppsEndpoint, self).handle_response(response)
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, self.response_model)


class CreateAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: CreateAppRequest,
        response_model=AppResponse,
    ):
        super(CreateAppEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data
        self.response_model = response_model

    def request_body(self):
        request_data = self.request_data.model_dump(
            by_alias=True, exclude_none=True
        )
        return json.dumps(request_data)

    def handle_response(self, response: HTTPResponse) -> AppResponse:
        try:
            super(CreateAppEndpoint, self).handle_response(response)
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, self.response_model)


class DeleteAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}"
    HTTP_METHOD = HTTPMethods.DELETE.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data):
        super(DeleteAppEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data

    def handle_response(self, response: HTTPResponse):
        try:
            super(DeleteAppEndpoint, self).handle_response(response)
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )


class GetAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self, project_id: str, request_data, response_model=AppResponse
    ):
        super(GetAppEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data
        self.response_model = response_model

    def handle_response(self, response: HTTPResponse) -> AppResponse:
        try:
            super(GetAppEndpoint, self).handle_response(response)
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, self.response_model)


class UpdateAppEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/apps/{app_id}"
    HTTP_METHOD = HTTPMethods.PATCH.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    QUERY_PARAM_FIELDS = {"update_mask"}

    def __init__(
        self,
        project_id: str,
        request_data: UpdateAppRequest,
        response_model=AppResponse,
    ):
        super(UpdateAppEndpoint, self).__init__(project_id, request_data)
        self.project_id = project_id
        self.request_data = request_data
        self.response_model = response_model

    def build_query_params(self) -> dict:
        body_data = self._build_body_data()
        if not body_data:
            return {}
        return {"update_mask": ",".join(body_data.keys())}

    def request_body(self):
        return json.dumps(self._build_body_data())

    def _build_body_data(self) -> dict:
        path_params = self._get_path_params_from_url()
        exclude_set = path_params.union(self.QUERY_PARAM_FIELDS)
        return self.request_data.model_dump(
            by_alias=True, exclude_none=True, exclude=exclude_set
        )

    def handle_response(self, response: HTTPResponse) -> AppResponse:
        try:
            super(UpdateAppEndpoint, self).handle_response(response)
        except ConversationException as e:
            raise ConversationException(
                message=e.args[0],
                response=e.http_response,
                is_from_server=e.is_from_server,
            )
        return self.process_response_model(response.body, self.response_model)
