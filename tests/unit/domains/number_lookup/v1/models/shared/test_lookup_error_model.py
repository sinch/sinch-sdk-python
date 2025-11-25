from sinch.domains.number_lookup.models.v1.shared import LookupError


def test_lookup_error_valid_expects_parsed_data():
    """
    Test a valid instance of LookupError
    """
    data = {
        "status": 100,
        "title": "Feature Disabled",
        "detail": "VoIPDetection feature is currently disabled.",
        "type": "validation_error",
    }
    error = LookupError(**data)

    assert error.status == 100
    assert error.title == "Feature Disabled"
    assert error.detail == "VoIPDetection feature is currently disabled."
    assert error.type == "validation_error"


def test_lookup_error_optional_fields_expects_parsed_data():
    """
    Test missing optional fields in LookupError
    """
    data = {}
    error = LookupError(**data)

    assert error.status is None
    assert error.title is None
    assert error.detail is None
    assert error.type is None
