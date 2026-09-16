import uuid

import pytest

from sinch.domains.voice import Voice
from sinch.domains.voice.api.v2.batches_apis import Batches
from sinch.domains.voice.api.v2.internal.batches_endpoints import (
    GetBatchCallSummaryEndpoint,
    GetBatchDetailsEndpoint,
    StartBatchEndpoint,
    StopBatchProcessingEndpoint,
)
from sinch.domains.voice.models.v2.batches.internal.request.batch_id_request import (
    BatchIdRequest,
)
from sinch.domains.voice.models.v2.batches.internal.request.start_batch_request import (
    StartBatchRequest,
)
from sinch.domains.voice.models.v2.batches.response.batch_details_response import (
    BatchDetailsResponse,
)
from sinch.domains.voice.models.v2.batches.response.batch_stop_response import (
    BatchStopResponse,
)
from sinch.domains.voice.models.v2.batches.response.batch_summary_response import (
    BatchSummaryResponse,
)
from sinch.domains.voice.models.v2.batches.response.start_batch_response import (
    StartBatchResponse,
)
from sinch.domains.voice.models.v2.svaml.shared.dial_command import DialCommand


@pytest.fixture
def commands():
    return [
        {
            "command": "dial",
            "call_name": "origin",
            "from_": {"type": "PHONE", "phone": {"number": "+15551234567"}},
            "to": {"type": "PHONE", "phone": {"number": "@to_number"}},
            "events": {"on_hangup": [{"command": "hangup"}]},
        }
    ]


def test_voice_exposes_v2_batches(mock_sinch_client_voice):
    """Test that the domain class exposes the versioned batches resource."""
    assert isinstance(Voice(mock_sinch_client_voice).v2.batches, Batches)


def test_batches_start_expects_correct_request(
    mock_sinch_client_voice, commands, mocker
):
    """Test that all parameters of start are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        StartBatchResponse(
            projectId="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
            serviceId="6e124178-c29d-46a5-943c-5c2ae544aade",
            batchId="01BX5ZZKBKACTAV9WEVGEMMVRC",
        )
    )
    spy = mocker.spy(StartBatchEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.batches.start(
        commands=commands,
        parameters=[{"to_number": "+15559876544"}],
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        batch_options={"max_cps": 10, "ttl_seconds": 3600},
        idempotency_key="my-custom-key",
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, StartBatchRequest)
    assert request_data.commands[0] == DialCommand(
        command="dial",
        call_name="origin",
        from_={"type": "PHONE", "phone": {"number": "+15551234567"}},
        to={"type": "PHONE", "phone": {"number": "@to_number"}},
        events={"on_hangup": [{"command": "hangup"}]},
    )
    assert request_data.parameters == [{"to_number": "+15559876544"}]
    assert request_data.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert request_data.batch_options.max_cps == 10
    assert request_data.batch_options.ttl_seconds == 3600
    assert request_data.idempotency_key == "my-custom-key"
    assert isinstance(response, StartBatchResponse)
    assert response.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert response.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert response.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_batches_start_expects_omitted_optionals_unset(
    mock_sinch_client_voice, commands, mocker
):
    """Test that optional body parameters not passed by the caller stay unset."""
    spy = mocker.spy(StartBatchEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.batches.start(
        commands=commands, parameters=[{"to_number": "+15559876544"}]
    )

    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert "batch_options" not in request_data.model_fields_set


def test_batches_start_expects_omitted_optionals_with_default_values_to_be_generated(
    mock_sinch_client_voice, commands, mocker
):
    """Test that omited optional fields with default values are generated."""
    spy = mocker.spy(StartBatchEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.batches.start(
        commands=commands, parameters=[{"to_number": "+15559876544"}]
    )

    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert uuid.UUID(request_data.idempotency_key).version == 4


def test_batches_start_expects_extra_kwargs_forwarded(
    mock_sinch_client_voice, commands, mocker
):
    """Test that additional keyword arguments are forwarded to the request model."""
    spy = mocker.spy(StartBatchEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.batches.start(
        commands=commands,
        parameters=[{"to_number": "+15559876544"}],
        unexpected_field="unexpected_value",
    )

    _, kwargs = spy.call_args
    assert kwargs["request_data"].unexpected_field == "unexpected_value"


def test_batches_get_expects_correct_request(mock_sinch_client_voice, mocker):
    """Test that all parameters of get are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        BatchSummaryResponse(
            batch_id="01BX5ZZKBKACTAV9WEVGEMMVRC",
            session_count=3,
            queued=1,
            in_progress=1,
            completed=1,
            expired=0,
            requested_cps=10,
        )
    )
    spy = mocker.spy(GetBatchCallSummaryEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.batches.get(
        batch_id="01BX5ZZKBKACTAV9WEVGEMMVRC"
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, BatchIdRequest)
    assert request_data.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    assert isinstance(response, BatchSummaryResponse)
    assert response.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    assert response.session_count == 3
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_batches_get_details_expects_correct_request(
    mock_sinch_client_voice, mocker
):
    """Test that all parameters of get_details are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        BatchDetailsResponse(
            sessions=[
                {"id": "01F8Z5J4X2G9Y3J4X2G9Y3J4X2G9", "state": "COMPLETED"}
            ]
        )
    )
    spy = mocker.spy(GetBatchDetailsEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.batches.get_details(
        batch_id="01BX5ZZKBKACTAV9WEVGEMMVRC"
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, BatchIdRequest)
    assert request_data.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    assert isinstance(response, BatchDetailsResponse)
    assert response.sessions[0].id == "01F8Z5J4X2G9Y3J4X2G9Y3J4X2G9"
    assert response.sessions[0].state == "COMPLETED"
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_batches_stop_expects_correct_request(mock_sinch_client_voice, mocker):
    """Test that all parameters of stop are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        BatchStopResponse(result="STOP_REQUESTED")
    )
    spy = mocker.spy(StopBatchProcessingEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.batches.stop(
        batch_id="01BX5ZZKBKACTAV9WEVGEMMVRC"
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, BatchIdRequest)
    assert request_data.batch_id == "01BX5ZZKBKACTAV9WEVGEMMVRC"
    assert isinstance(response, BatchStopResponse)
    assert response.result == "STOP_REQUESTED"
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()
