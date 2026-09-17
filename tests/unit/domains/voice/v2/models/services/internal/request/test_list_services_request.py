from sinch.domains.voice.models.v2.services.internal.request.list_services_request import (
    ListServicesRequest,
)


def test_list_services_request_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = ListServicesRequest(
        filter="Primary",
        is_default=True,
        page_size=20,
        page=1,
    )

    assert model.filter == "Primary"
    assert model.is_default is True
    assert model.page_size == 20
    assert model.page == 1

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert alias_dump["filter"] == "Primary"
    assert alias_dump["isDefault"] is True
    assert alias_dump["pageSize"] == 20
    assert alias_dump["page"] == 1


def test_list_services_request_expects_all_optionals_default_to_none():
    """Test that all optional fields default to None."""
    model = ListServicesRequest()

    assert model.filter is None
    assert model.is_default is None
    assert model.page_size is None
    assert model.page is None
