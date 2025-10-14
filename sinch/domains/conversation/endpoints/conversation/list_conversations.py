from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.domains.conversation.models.conversation.responses import SinchListConversationsResponse
from sinch.domains.conversation.models.conversation.requests import ListConversationsRequest
from sinch.domains.conversation.models.conversation import Conversation
from sinch.core.enums import HTTPAuthentication, HTTPMethods


class ListConversationsEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/conversations"
    HTTP_METHOD = HTTPMethods.GET.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(self, project_id: str, request_data: ListConversationsRequest):
        super(ListConversationsEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(origin=sinch.configuration.conversation_origin, project_id=self.project_id)

    def build_query_params(self):
        query_params = {}
        if self.request_data.app_id:
            query_params["app_id"] = self.request_data.app_id

        if self.request_data.contact_id:
            query_params["contact_id"] = self.request_data.contact_id

        if self.request_data.page_size:
            query_params["page_size"] = self.request_data.page_size

        if self.request_data.page_token:
            query_params["page_token"] = self.request_data.page_token

        return query_params

    def handle_response(self, response: HTTPResponse) -> SinchListConversationsResponse:
        super(ListConversationsEndpoint, self).handle_response(response)
        return SinchListConversationsResponse(
            conversations=[
                Conversation(
                    id=conversation["id"],
                    app_id=conversation["app_id"],
                    contact_id=conversation["contact_id"],
                    last_received=conversation["last_received"],
                    active_channel=conversation["active_channel"],
                    active=conversation["active"],
                    metadata=conversation["metadata"],
                    metadata_json=conversation["metadata_json"],
                )
                for conversation in response.body["conversations"]
            ],
            next_page_token=response.body["next_page_token"],
            total_size=response.body["total_size"],
        )
