import uuid
from datetime import datetime

import pytest

from sinch.core.pagination import LinkBasedPaginator
from sinch.domains.voice import Voice
from sinch.domains.voice.api.v2.calls_apis import Calls
from sinch.domains.voice.api.v2.internal.calls_endpoints import (
    GetCallByIdEndpoint,
    ListCallsEndpoint,
    PatchCallByIdEndpoint,
    PatchCallBySessionAndNameEndpoint,
    StartCallEndpoint,
)
from sinch.domains.voice.models.v2.calls.internal.list_calls_response import (
    ListCallsResponse,
)
from sinch.domains.voice.models.v2.calls.internal.request.call_id_request import (
    CallIdRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.list_calls_request import (
    ListCallsRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.patch_call_by_id_request import (
    PatchCallByIdRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.patch_call_by_session_and_name_request import (
    PatchCallBySessionAndNameRequest,
)
from sinch.domains.voice.models.v2.calls.internal.request.start_call_request import (
    StartCallRequest,
)
from sinch.domains.voice.models.v2.calls.response.start_call_response import (
    StartCallResponse,
)
from sinch.domains.voice.models.v2.shared.call import Call
from sinch.domains.voice.models.v2.shared.pagination_links import (
    PaginationLinks,
)
from sinch.domains.voice.models.v2.shared.pagination_meta import (
    PaginationMeta,
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
        )
    )
    spy = mocker.spy(StartCallEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.calls.start(
        commands=commands,
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        idempotency_key="my-custom-key",
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
    assert isinstance(response, StartCallResponse)
    assert response.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert response.project_id == "5c5bf2b1-35ae-4825-ab89-457e07bb60e6"
    assert response.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert request_data.idempotency_key == "my-custom-key"
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_calls_start_expects_omitted_optionals_with_default_values_to_be_generated(
    mock_sinch_client_voice, commands, mocker
):
    """Test that omited optional fields with default values are generated."""
    spy = mocker.spy(StartCallEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.calls.start(commands=commands)

    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert uuid.UUID(request_data.idempotency_key).version == 4


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


@pytest.fixture
def mock_list_calls_response():
    return ListCallsResponse(
        calls=[],
        links=PaginationLinks(
            first="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=1&pageSize=20",
            last="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=5&pageSize=20",
            self="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls?page=2&pageSize=20",
        ),
        meta=PaginationMeta(totalCount=100, pageCount=5),
    )


def test_calls_list_expects_correct_request(
    mock_sinch_client_voice, mock_list_calls_response, mocker
):
    """Test that all parameters of list are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        mock_list_calls_response
    )
    spy = mocker.spy(ListCallsEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.calls.list(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        from_="+15551234567",
        to="+15551234568",
        call_type="PHONE",
        start_time=datetime(2025, 2, 1, 14, 0, 0),
        end_time=datetime(2025, 3, 1, 14, 0, 0),
        call_result="COMPLETED",
        call_reason="CALLEE_HANGUP",
        page_size=20,
        page=2,
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, ListCallsRequest)
    assert request_data.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert request_data.from_ == "+15551234567"
    assert request_data.to == "+15551234568"
    assert request_data.call_type == "PHONE"
    assert request_data.start_time == datetime(2025, 2, 1, 14, 0, 0)
    assert request_data.end_time == datetime(2025, 3, 1, 14, 0, 0)
    assert request_data.call_result == "COMPLETED"
    assert request_data.call_reason == "CALLEE_HANGUP"
    assert request_data.page_size == 20
    assert request_data.page == 2
    assert isinstance(response, LinkBasedPaginator)
    assert response.result == mock_list_calls_response
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_calls_get_expects_correct_request(mock_sinch_client_voice, mocker):
    """Test that call_id is mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = Call(
        callId="01ARZ3NDEKTSV4RRFFQ69G5FAA",
        projectId="5c5bf2b1-35ae-4825-ab89-457e07bb60e6",
        serviceId="6e124178-c29d-46a5-943c-5c2ae544aade",
        sessionId="01BX5ZZKBKACTAV9WEVGEMMVRB",
        startTime="2025-02-10T09:00:00Z",
        callType="PHONE",
        direction="OUTBOUND",
        callResult="COMPLETED",
        originationType="SERVER",
        callRate={"currencyCode": "USD", "amount": "0.0123"},
        callResourceUrl="https://voice.api.sinch.com/v2/projects/5c5bf2b1-35ae-4825-ab89-457e07bb60e6/calls/01ARZ3NDEKTSV4RRFFQ69G5FAA",
    )
    spy = mocker.spy(GetCallByIdEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.calls.get(
        call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA"
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, CallIdRequest)
    assert request_data.call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert isinstance(response, Call)
    assert response.call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_calls_interact_by_call_id_expects_correct_request(
    mock_sinch_client_voice, mocker
):
    """Test that call_id and commands are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = None
    spy = mocker.spy(PatchCallByIdEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.calls.interact_by_call_id(
        call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA",
        commands=[{"command": "hangup"}],
        idempotency_key="my-custom-key",
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, PatchCallByIdRequest)
    assert request_data.call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert request_data.commands[0].command == "hangup"
    assert request_data.idempotency_key == "my-custom-key"
    assert response is None
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_calls_interact_by_call_id_expects_omitted_optionals_with_default_values_to_be_generated(
    mock_sinch_client_voice, mocker
):
    """Test that omitted optional fields with default values are generated."""
    spy = mocker.spy(PatchCallByIdEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.calls.interact_by_call_id(
        call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA",
        commands=[{"command": "hangup"}],
    )

    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert uuid.UUID(request_data.idempotency_key).version == 4


def test_calls_interact_by_call_id_expects_extra_kwargs_forwarded(
    mock_sinch_client_voice, mocker
):
    """Test that additional keyword arguments are forwarded to the request model."""
    spy = mocker.spy(PatchCallByIdEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.calls.interact_by_call_id(
        call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA",
        commands=[{"command": "hangup"}],
        unexpected_field="unexpected_value",
    )

    _, kwargs = spy.call_args
    assert kwargs["request_data"].unexpected_field == "unexpected_value"


def test_calls_interact_by_call_name_expects_correct_request(
    mock_sinch_client_voice, mocker
):
    """Test that session_id, call_name and commands are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = None
    spy = mocker.spy(PatchCallBySessionAndNameEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.calls.interact_by_call_name(
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        call_name="origin",
        commands=[{"command": "hangup"}],
        idempotency_key="my-custom-key",
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, PatchCallBySessionAndNameRequest)
    assert request_data.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert request_data.call_name == "origin"
    assert request_data.commands[0].command == "hangup"
    assert request_data.idempotency_key == "my-custom-key"
    assert response is None
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_calls_interact_by_call_name_expects_omitted_optionals_with_default_values_to_be_generated(
    mock_sinch_client_voice, mocker
):
    """Test that omitted optional fields with default values are generated."""
    spy = mocker.spy(PatchCallBySessionAndNameEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.calls.interact_by_call_name(
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        call_name="origin",
        commands=[{"command": "hangup"}],
    )

    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert uuid.UUID(request_data.idempotency_key).version == 4


def test_calls_interact_by_call_name_expects_extra_kwargs_forwarded(
    mock_sinch_client_voice, mocker
):
    """Test that additional keyword arguments are forwarded to the request model."""
    spy = mocker.spy(PatchCallBySessionAndNameEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.calls.interact_by_call_name(
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        call_name="origin",
        commands=[{"command": "hangup"}],
        unexpected_field="unexpected_value",
    )

    _, kwargs = spy.call_args
    assert kwargs["request_data"].unexpected_field == "unexpected_value"
