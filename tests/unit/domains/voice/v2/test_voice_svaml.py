from sinch.domains.voice import Voice
from sinch.domains.voice.api.v2.internal.svaml_endpoints import (
    DescribeSvamlEndpoint,
    ValidateSvamlEndpoint,
)
from sinch.domains.voice.api.v2.svaml_apis import Svaml
from sinch.domains.voice.models.v2.svaml.internal.request.describe_svaml_request import (
    DescribeSvamlRequest,
)
from sinch.domains.voice.models.v2.svaml.internal.request.validate_svaml_request import (
    ValidateSvamlRequest,
)
from sinch.domains.voice.models.v2.svaml.response.describe_svaml_response import (
    DescribeSvamlResponse,
)
from sinch.domains.voice.models.v2.svaml.response.validate_svaml_response import (
    ValidateSvamlResponse,
)


def test_voice_exposes_v2_svaml(mock_sinch_client_voice):
    """Test that the domain class exposes the versioned svaml resource."""
    assert isinstance(Voice(mock_sinch_client_voice).v2.svaml, Svaml)


def test_svaml_describe_expects_correct_request(
    mock_sinch_client_voice, mocker
):
    """Test that all parameters of describe are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = DescribeSvamlResponse(
        description="The call is answered and a TTS message is played using the voice Emma."
    )
    spy = mocker.spy(DescribeSvamlEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.svaml.describe(
        commands=[
            {"command": "answer"},
            {
                "command": "messages",
                "messages": [
                    {
                        "type": "SAY",
                        "say": {
                            "text": "Welcome to ACME support.",
                            "voiceName": "Emma",
                        },
                    }
                ],
            },
        ],
        call_name="incoming",
        on_hangup=[{"command": "hangup"}],
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, DescribeSvamlRequest)
    assert request_data.svaml.commands[0].command == "answer"
    assert request_data.svaml.call_name == "incoming"
    assert request_data.svaml.events.on_hangup[0].command == "hangup"
    assert isinstance(response, DescribeSvamlResponse)
    assert response.description == (
        "The call is answered and a TTS message is played using the voice Emma."
    )
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_svaml_validate_expects_correct_request(
    mock_sinch_client_voice, mocker
):
    """Test that all parameters of validate are mapped onto the request model."""
    mock_sinch_client_voice.configuration.transport.request.return_value = (
        ValidateSvamlResponse(isValid=True)
    )
    spy = mocker.spy(ValidateSvamlEndpoint, "__init__")

    response = Voice(mock_sinch_client_voice).v2.svaml.validate(
        commands=[{"command": "answer"}],
        call_name="incoming",
        on_hangup=[{"command": "hangup"}],
        validation_type="STRICT",
    )

    spy.assert_called_once()
    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert kwargs["project_id"] == "test_project_id"
    assert isinstance(request_data, ValidateSvamlRequest)
    assert request_data.svaml.commands[0].command == "answer"
    assert request_data.svaml.call_name == "incoming"
    assert request_data.svaml.events.on_hangup[0].command == "hangup"
    assert request_data.validation_type == "STRICT"
    assert isinstance(response, ValidateSvamlResponse)
    assert response.is_valid is True
    mock_sinch_client_voice.configuration.transport.request.assert_called_once()


def test_svaml_validate_expects_omitted_optionals_unset(
    mock_sinch_client_voice, mocker
):
    """Test that omitted optional fields never reach the request model."""
    spy = mocker.spy(ValidateSvamlEndpoint, "__init__")

    Voice(mock_sinch_client_voice).v2.svaml.validate(
        commands=[{"command": "answer"}],
    )

    _, kwargs = spy.call_args
    request_data = kwargs["request_data"]
    assert "validation_type" not in request_data.model_fields_set
    assert "call_name" not in request_data.svaml.model_fields_set
    assert "events" not in request_data.svaml.model_fields_set
