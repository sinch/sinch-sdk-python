import pytest

from sinch.domains.voice import Voice
from sinch.domains.voice.api.v2.calls_apis import Calls
from sinch.domains.voice.api.v2.internal.calls_endpoints import (
    StartCallEndpoint,
)
from sinch.domains.voice.models.v2.calls.internal.request.start_call_request import (
    StartCallRequest,
)
from sinch.domains.voice.models.v2.calls.response.start_call_response import (
    StartCallResponse,
)
from sinch.domains.voice.models.v2.svaml.shared.dial_command import DialCommand


@pytest.fixture
def commands():
    return [
        {
            "command": "dial",
            "call_name": "origin",
            "from_": {"type": "PHONE", "phone": {"number": "+15551234567"}},
            "to": {"type": "PHONE", "phone": {"number": "+15559876543"}},
            "events": {"on_hangup": [{"command": "hangup"}]},
        }
    ]


def test_voice_exposes_v2_calls(mock_sinch_client_voice):
    """Test that the domain class exposes the versioned calls resource."""
    assert isinstance(Voice(mock_sinch_client_voice).v2.calls, Calls)


def test_calls_start_expects_correct_request(
    mock_sinch_client_voice, commands, mocker
):
    """Test that all parameters of create are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        StartCallResponse(
            projectId="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            serviceId="6e124178-c29d-46a5-943c-5c2ae544aade",
            sessionId="01BX5ZZKBKACTAV9WEVGEMMVRB",
            batchId="01BX5ZZKBKACTAV9WEVGEMMVRC",
        )
    )
    spy = mocker.spy(StartCallEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.calls.start(
        commands=commands,
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        parameters=[{"numberB": "+15559876544"}],
        batch_options={"max_cps": 10, "ttl_seconds": 3600},
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, StartCallRequest)
    assert request_data.commands[0] == DialCommand(
        command="dial",
        call_name="origin",
        from_={"type": "PHONE", "phone": {"number": "+15551234567"}},
        to={"type": "PHONE", "phone": {"number": "+15559876543"}},
        events={"on_hangup": [{"command": "hangup"}]},
    )
    assert request_data.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert request_data.parameters == [{"numberB": "+15559876544"}]
    assert request_data.batch_options.max_cps == 10
    assert request_data.batch_options.ttl_seconds == 3600
    assert isinstance(response, StartCallResponse)
    assert response.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert response.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert response.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert response.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_calls_start_expects_omitted_optionals_unset(
    mock_sinch_client_voice, commands, mocker
):
    """Test that optional body parameters not passed by the caller stay unset."""
    spy = mocker.spy(StartCallEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.calls.start(commands=commands)

    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert "parameters" not in request_data.model_fields_set
    assert "batch_options" not in request_data.model_fields_set


def test_calls_start_expects_extra_kwargs_forwarded(
    mock_sinch_client_voice, commands, mocker
):
    """Test that additional keyword arguments are forwarded to the request model."""
    spy = mocker.spy(StartCallEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.calls.start(
        commands=commands, unexpected_field="unexpected_value"
    )

    _, kwargs = spy.call_args
    assert kwargs["request_data"].unexpected_field == "unexpected_value"
