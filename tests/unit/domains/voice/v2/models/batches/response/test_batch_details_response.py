from sinch.domains.voice.models.v2.batches.response.batch_details_response import (
    BatchDetailsResponse,
    BatchSessionSummary,
)


def test_batch_details_response_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = BatchDetailsResponse(
        sessions=[
            {"id": "01F8Z5J4X2G9Y3J4X2G9Y3J4X2G9", "state": "COMPLETED"},
            {"id": "01F8Z5J4X2G9Y3J4X2G9Y3J4X5YJ", "state": "IN_PROGRESS"},
        ]
    )

    assert len(model.sessions) == 2
    assert isinstance(model.sessions[0], BatchSessionSummary)
    assert model.sessions[0].id == "01F8Z5J4X2G9Y3J4X2G9Y3J4X2G9"
    assert model.sessions[0].state == "COMPLETED"
    assert model.sessions[1].state == "IN_PROGRESS"



def test_batch_session_summary_expects_all_optionals_default_to_none():
    """Test that all optional fields of BatchSessionSummary default to None."""
    model = BatchSessionSummary()

    assert model.id is None
    assert model.state is None
