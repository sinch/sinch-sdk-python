import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.contacts.internal.merge_contact_request import (
    MergeContactRequest,
)


def test_merge_contact_request_expects_required_fields_parsed():
    """Test that destination_id and source_id are read back correctly."""
    request = MergeContactRequest(
        destination_id="01W4FFL35P4NC4K35CONTACT002",
        source_id="01W4FFL35P4NC4K35CONTACT001",
    )

    assert request.destination_id == "01W4FFL35P4NC4K35CONTACT002"
    assert request.source_id == "01W4FFL35P4NC4K35CONTACT001"
    assert request.strategy is None


def test_merge_contact_request_expects_strategy_parsed():
    """Test that strategy is read back correctly when set."""
    request = MergeContactRequest(
        destination_id="01W4FFL35P4NC4K35CONTACT002",
        source_id="01W4FFL35P4NC4K35CONTACT001",
        strategy="MERGE",
    )

    assert request.strategy == "MERGE"


def test_merge_contact_request_expects_error_when_source_id_missing():
    """Test that source_id is required."""
    with pytest.raises(ValidationError):
        MergeContactRequest(destination_id="01W4FFL35P4NC4K35CONTACT002")


def test_merge_contact_request_expects_error_when_destination_id_missing():
    """Test that destination_id is required."""
    with pytest.raises(ValidationError):
        MergeContactRequest(source_id="01W4FFL35P4NC4K35CONTACT001")
