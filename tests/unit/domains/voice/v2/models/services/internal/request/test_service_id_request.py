from sinch.domains.voice.models.v2.services.internal.request.service_id_request import (
    ServiceIdRequest,
)


def test_service_id_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ServiceIdRequest(
        service_id="6e124178-c29d-46a5-943c-5c2ae544aade"
    )

    assert model.service_id == "6e124178-c29d-46a5-943c-5c2ae544aade"

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["serviceId"] == "6e124178-c29d-46a5-943c-5c2ae544aade"
