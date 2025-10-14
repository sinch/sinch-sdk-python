from sinch.domains.numbers.models.v1.internal import ListAvailableRegionsRequest


def test_list_available_regions_request_expects_parsed_input():
    """
    Test that the model correctly parses input with valid number types.
    """
    data = {"types": ["MOBILE", "LOCAL", "TOLL_FREE"]}

    request = ListAvailableRegionsRequest(**data)
    assert request.types == ["MOBILE", "LOCAL", "TOLL_FREE"]


def test_list_available_regions_request_expects_optional_fields_handled():
    """
    Test that optional fields are properly handled when not provided.
    """
    data = {}
    request = ListAvailableRegionsRequest(**data)
    assert request.types is None


def test_list_available_regions_request_expects_validation_for_extra_type():
    """
    Test that validation errors are raised for invalid number types.
    """
    data = {"types": ["EXTRA_TYPE"]}
    request = ListAvailableRegionsRequest(**data)
    assert request.types == ["EXTRA_TYPE"]
