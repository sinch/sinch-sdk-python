import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.consents.internal.list_audit_records_request import (
    ListAuditRecordsRequest,
)


def test_list_audit_records_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListAuditRecordsRequest(
        app_id="01W4FFL35P4NC4K35CONVAPP001", identity="33612345678"
    )

    assert model.app_id == "01W4FFL35P4NC4K35CONVAPP001"
    assert model.identity == "33612345678"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump == {
        "app_id": "01W4FFL35P4NC4K35CONVAPP001",
        "identity": "33612345678",
    }


@pytest.mark.parametrize("missing", ["app_id", "identity"])
def test_list_audit_records_request_expects_missing_required_field_rejected(
    missing,
):
    """Test that the model rejects input missing a required field."""
    data = {"app_id": "APP123", "identity": "33612345678"}
    del data[missing]

    with pytest.raises(ValidationError):
        ListAuditRecordsRequest(**data)
