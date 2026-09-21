import uuid

import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.calls.internal.request.patch_call_by_session_and_name_request import (
    PatchCallBySessionAndNameRequest,
)
from sinch.domains.voice.models.v2.svaml.shared.hangup_command import (
    HangupCommand,
)

COMMANDS = [{"command": "hangup"}]


def test_patch_call_by_session_and_name_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = PatchCallBySessionAndNameRequest(
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        call_name="origin",
        commands=COMMANDS,
        idempotency_key="my-custom-key",
    )

    assert model.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert model.call_name == "origin"
    assert isinstance(model.commands[0], HangupCommand)

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["sessionId"] == "01BX5ZZKBKACTAV9WEVGEMMVRB"
    assert alias_dump["callName"] == "origin"
    assert alias_dump["Idempotency-Key"] == "my-custom-key"


def test_patch_call_by_session_and_name_request_expects_idempotency_key_default_generated():
    """Test that the idempotency key defaults to a generated UUID v4."""
    model = PatchCallBySessionAndNameRequest(
        session_id="01BX5ZZKBKACTAV9WEVGEMMVRB",
        call_name="origin",
        commands=COMMANDS,
    )

    assert uuid.UUID(model.idempotency_key).version == 4


def test_patch_call_by_session_and_name_request_expects_validation_error_for_missing_required():
    """Test that session_id, call_name and commands are required."""
    with pytest.raises(ValidationError):
        PatchCallBySessionAndNameRequest()
