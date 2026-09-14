from sinch.domains.voice.models.v2.sessions.internal.request.session_id_request import (
    SessionIdRequest,
)


def test_session_id_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = SessionIdRequest(session_id="01BX5ZZKBKACTAV9WEVGEMMVRB")

    assert model.session_id == "01BX5ZZKBKACTAV9WEVGEMMVRB"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["sessionId"] == "01BX5ZZKBKACTAV9WEVGEMMVRB"

