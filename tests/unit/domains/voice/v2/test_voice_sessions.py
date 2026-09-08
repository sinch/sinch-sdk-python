from sinch.domains.voice import Voice
from sinch.domains.voice.api.v2.internal.sessions_endpoints import (
    GetSessionEndpoint,
)
from sinch.domains.voice.api.v2.sessions_apis import Sessions
from sinch.domains.voice.models.v2.sessions.internal.request.session_id_request import (
    SessionIdRequest,
)
from sinch.domains.voice.models.v2.sessions.response.session_response import (
    SessionResponse,
)


def test_voice_exposes_v2_sessions(mock_sinch_client_voice):
    """Test that the domain class exposes the versioned sessions resource."""
    assert isinstance(Voice(mock_sinch_client_voice).v2.sessions, Sessions)


def test_sessions_get_expects_correct_request(mock_sinch_client_voice, mocker):
    """Test that all parameters of get are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        SessionResponse(
            session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
            project_id="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
            state="COMPLETED",
            calls=[],
            create_time="2024-06-05T12:00:00Z",
        )
    )
    spy = mocker.spy(GetSessionEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.sessions.get(
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB"
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, SessionIdRequest)
    assert request_data.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert isinstance(response, SessionResponse)
    assert response.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert response.state == "COMPLETED"
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()

