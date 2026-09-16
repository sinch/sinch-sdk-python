import uuid

import pytest
from pydantic import ValidationError

from sinch.domains.voice.models.v2.batches.internal.request.start_batch_request import (
    StartBatchRequest,
)
from sinch.domains.voice.models.v2.batches.shared.batch_options import (
    BatchOptions,
)
from sinch.domains.voice.models.v2.svaml.shared.dial_command import DialCommand

COMMANDS = [
    {
        "command": "dial",
        "call_name": "origin",
        "to": {"type": "PHONE", "phone": {"number": "@to_number"}},
    }
]
PARAMETERS = [{"to_number": "+15559876543"}]


def test_start_batch_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = StartBatchRequest(
        commands=COMMANDS,
        parameters=PARAMETERS,
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade",
        batch_options={"max_cps": 10, "ttl_seconds": 3600},
        idempotency_key="my-custom-key",
    )

    assert isinstance(model.commands[0], DialCommand)
    assert model.commands[0].call_name == "origin"
    assert model.parameters == PARAMETERS
    assert model.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert isinstance(model.batch_options, BatchOptions)
    assert model.batch_options.max_cps == 10
    assert model.batch_options.ttl_seconds == 3600

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
    assert alias_dump["batchOptions"] == {"maxCps": 10, "ttlSeconds": 3600}
    assert alias_dump["Idempotency-Key"] == "my-custom-key"


def test_start_batch_request_expects_all_optionals_default_to_defaults():
    """Test that all optional fields default to their expected default values."""
    model = StartBatchRequest(commands=COMMANDS, parameters=PARAMETERS)

    assert model.service_id is None
    assert model.batch_options is None
    assert uuid.UUID(model.idempotency_key).version == 4


def test_start_batch_request_expects_validation_error_for_missing_required():
    """Test that commands and parameters are required."""
    with pytest.raises(ValidationError):
        StartBatchRequest()

    with pytest.raises(ValidationError):
        StartBatchRequest(commands=COMMANDS)
