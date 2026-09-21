import uuid

import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.calls.internal.request.start_call_request import (
    StartCallRequest,
)
from sinch.domains.voice.models.v2.svaml.shared.dial_command import DialCommand

COMMANDS = [
    {
        "command": "dial",
        "call_name": "origin",
        "to": {"type": "PHONE", "phone": {"number": "+15559876543"}},
    }
]


def test_start_call_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StartCallRequest(
        commands=COMMANDS,
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        idempotency_key="my-custom-key",
    )

    assert isinstance(model.commands[0], DialCommand)
    assert model.commands[0].call_name == "origin"
    assert model.commands[0].to.phone.number == "+15559876543"
    assert model.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert alias_dump["Idempotency-Key"] == "my-custom-key"


def test_start_call_request_expects_all_optionals_default_to_defaults():
    """Test that all optional fields default to their expected default values."""
    model = StartCallRequest(commands=COMMANDS)

    assert model.service_id is None
    assert uuid.UUID(model.idempotency_key).version == 4


def test_start_call_request_expects_validation_error_for_missing_required():
    """Test that commands is required."""
    with pytest.raises(ValidationError):
        StartCallRequest()
