from sinch.domains.conversation.api.v1.internal.messages_endpoints import GetMessageEndpoint
from sinch.domains.conversation.models.v1.messages.internal.request import MessageIdRequest


def test_user_agent_header_creation_expects_to_be_included(sinch_client_sync):
    """Test that User-Agent header is created when preparing a conversation endpoint request"""
    sinch_client_sync.configuration.conversation_region = "eu"
    
    request_data = MessageIdRequest(message_id="test_message_id")
    http_endpoint = GetMessageEndpoint(
        project_id=sinch_client_sync.configuration.project_id,
        request_data=request_data
    )
    
    http_request = sinch_client_sync.configuration.transport.prepare_request(http_endpoint)
    
    assert "User-Agent" in http_request.headers
    assert "sinch-sdk" in http_request.headers["User-Agent"]
