from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.consents.response.audit_record_response import (
    AuditRecordResponse,
)

FULL_INPUT = {
    "origin": "ORIGIN_MO",
    "operation": "OPERATION_INSERT",
    "list_type": "OPT_OUT_ALL",
    "project_id": "test_project_id",
    "app_id": "01W4FFL35P4NC4K35CONVAPP001",
    "datetime": "2025-06-06T14:42:56Z",
}


def test_audit_record_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = AuditRecordResponse(**FULL_INPUT)

    assert model.origin == "ORIGIN_MO"
    assert model.operation == "OPERATION_INSERT"
    assert model.list_type == "OPT_OUT_ALL"
    assert model.project_id == "test_project_id"
    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.datetime == datetime(
        2025, 6, 6, 14, 42, 56, tzinfo=timezone.utc
    )

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump == FULL_INPUT


def test_audit_record_response_expects_unknown_enum_values_accepted():
    """Test that values outside the known enums are still accepted."""
    model = AuditRecordResponse(
        **{
            **FULL_INPUT,
            "origin": "ORIGIN_FUTURE",
            "operation": "OPERATION_FUTURE",
            "list_type": "OPT_OUT_FUTURE",
        }
    )

    assert model.origin == "ORIGIN_FUTURE"
    assert model.operation == "OPERATION_FUTURE"
    assert model.list_type == "OPT_OUT_FUTURE"


@pytest.mark.parametrize("missing", list(FULL_INPUT))
def test_audit_record_response_expects_missing_required_field_rejected(
    missing,
):
    """Test that the model rejects input missing a required field."""
    data = {k: v for k, v in FULL_INPUT.items() if k != missing}

    with pytest.raises(ValidationError):
        AuditRecordResponse(**data)
