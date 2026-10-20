from datetime import datetime, timezone

from sinch.domains.conversation.models.v1.consents.response.audit_record_response import (
    AuditRecordResponse,
)
from sinch.domains.conversation.models.v1.consents.response.audit_records_response import (
    AuditRecordsResponse,
)
from sinch.domains.conversation.models.v1.consents.response.consent_identity_response import (
    ConsentIdentityResponse,
)


def test_audit_records_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = AuditRecordsResponse(
        identity={"identity": "33612345678"},
        audit_records=[
            {
                "origin": "ORIGIN_API",
                "operation": "OPERATION_DELETE",
                "list_type": "OPT_OUT_NOTIFICATION",
                "project_id": "test_project_id",
                "app_id": "01W4FFL35P4NC4K35CONVAPP001",
                "datetime": "2025-06-06T14:42:56Z",
            }
        ],
    )

    assert isinstance(model.identity, ConsentIdentityResponse)
    assert model.identity.identity == "33612345678"
    assert len(model.audit_records) == 1
    record = model.audit_records[0]
    assert isinstance(record, AuditRecordResponse)
    assert record.origin == "ORIGIN_API"
    assert record.operation == "OPERATION_DELETE"
    assert record.list_type == "OPT_OUT_NOTIFICATION"
    assert record.datetime == datetime(
        2025, 6, 6, 14, 42, 56, tzinfo=timezone.utc
    )

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    assert alias_dump["identity"] == {"identity": "33612345678"}
    assert alias_dump["audit_records"][0]["datetime"] == "2025-06-06T14:42:56Z"


def test_audit_records_response_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = AuditRecordsResponse()

    assert model.identity is None
    assert model.audit_records is None
