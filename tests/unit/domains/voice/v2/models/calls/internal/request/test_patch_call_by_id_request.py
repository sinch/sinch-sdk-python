import uuid

import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.calls.internal.request.patch_call_by_id_request import (
    PatchCallByIdRequest,
)
from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)

COMMANDS = [{"command": "hangup"}]


def test_patch_call_by_id_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = PatchCallByIdRequest(
        call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA",
        commands=COMMANDS,
        idempotency_key="my-custom-key",
    )

    assert model.call_id == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert isinstance(model.commands[0], HangupCommand)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["callId"] == "01ARZ3NDEKTSV4RRFFQ69G5FAA"
    assert alias_dump["Idempotency-Key"] == "my-custom-key"


def test_patch_call_by_id_request_expects_idempotency_key_default_generated():
    """Test that the idempotency key defaults to a generated UUID v4."""
    model = PatchCallByIdRequest(
        call_id="01ARZ3NDEKTSV4RRFFQ69G5FAA", commands=COMMANDS
    )

    assert uuid.UUID(model.idempotency_key).version == 4


def test_patch_call_by_id_request_expects_validation_error_for_missing_required():
    """Test that call_id and commands are required."""
    with pytest.raises(ValidationError):
        PatchCallByIdRequest()
