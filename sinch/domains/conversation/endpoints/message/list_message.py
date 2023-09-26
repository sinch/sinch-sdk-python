from sinch.core.models.http_response import HTTPResponse
from sinch.domains.conversation.endpoints.conversation_endpoint import ConversationEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethod
from sinch.domains.conversation.models import SinchConversationMessage
from sinch.domains.conversation.models.message.responses import ListConversationMessagesResponse
from sinch.domains.conversation.models.message.requests import ListConversationMessagesRequest


class ListConversationMessagesEndpoint(ConversationEndpoint):
    ENDPOINT_URL = "{origin}/v1/projects/{project_id}/messages"
    HTTP_METHOD = HTTPMethod.GET
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH

    def __init__(self, project_id: str, request_data: ListConversationMessagesRequest):
        super(ListConversationMessagesEndpoint, self).__init__(project_id, request_data)
        self.request_data = request_data
        self.project_id = project_id

    def build_url(self, sinch):
        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id
        )

    def build_query_params(self):
        query_params = {}
        if self.request_data.conversation_id:
            query_params["conversation_id"] = self.request_data.conversation_id

        if self.request_data.contact_id:
            query_params["contact_id"] = self.request_data.contact_id

        if self.request_data.page_size:
            query_params["page_size"] = self.request_data.page_size

        if self.request_data.page_token:
            query_params["page_token"] = self.request_data.page_token

        if self.request_data.app_id:
            query_params["app_id"] = self.request_data.app_id

        if self.request_data.view:
            query_params["view"] = self.request_data.view

        if self.request_data.messages_source:
            query_params["messages_source"] = self.request_data.messages_source

        if self.request_data.only_recipient_originated:
            query_params["only_recipient_originated"] = self.request_data.only_recipient_originated

        return query_params

    def handle_response(self, response: HTTPResponse) -> ListConversationMessagesResponse:
        super(ListConversationMessagesEndpoint, self).handle_response(response)
        return ListConversationMessagesResponse(
            messages=[
                SinchConversationMessage(
                    id=message["id"],
                    direction=message["direction"],
                    channel_identity=message["channel_identity"],
                    app_message=message["app_message"],
                    conversation_id=message["conversation_id"],
                    contact_id=message["contact_id"],
                    metadata=message["metadata"],
                    accept_time=message["accept_time"],
                    sender_id=message["sender_id"],
                    processing_mode=message["processing_mode"]
                ) for message in response.body["messages"]
            ],
            next_page_token=response.body.get("next_page_token")
        )
