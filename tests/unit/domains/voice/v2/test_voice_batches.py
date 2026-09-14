from sinch.domains.voice import Voice
from sinch.domains.voice.api.v2.batches_apis import Batches
from sinch.domains.voice.api.v2.internal.batches_endpoints import (
    GetBatchCallSummaryEndpoint,
    GetBatchDetailsEndpoint,
    StopBatchProcessingEndpoint,
)
from sinch.domains.voice.models.v2.batches.internal.request.batch_id_request import (
    BatchIdRequest,
)
from sinch.domains.voice.models.v2.batches.response.batch_details_response import (
    BatchDetailsResponse,
)
from sinch.domains.voice.models.v2.batches.response.batch_summary_response import (
    BatchSummaryResponse,
)


def test_voice_exposes_v2_batches(mock_sinch_client_voice):
    """Test that the domain class exposes the versioned batches resource."""
    assert isinstance(Voice(mock_sinch_client_voice).v2.batches, Batches)


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
            sessions=[{"id": "01F8Z5J4X2G9Y3J4X2G9Y3J4X2G9", "state": "COMPLETED"}]
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
    mock_sinch_client_voice.configuration.transport.request.return_value = None
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
    assert response is None
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()
