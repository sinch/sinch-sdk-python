from sinch.domains.conversation.endpoints.app.delete_app import DeleteConversationAppEndpoint
from sinch.domains.conversation.models.app.requests import DeleteConversationAppRequest


def test_user_agent_header_creation(sinch_client_sync):
    endpoint = DeleteConversationAppRequest(app_id="42")
    http_endpoint = DeleteConversationAppEndpoint(sinch_client_sync, endpoint)
    http_request = sinch_client_sync.configuration.transport.prepare_request(http_endpoint)
    assert "User-Agent" in http_request.headers
