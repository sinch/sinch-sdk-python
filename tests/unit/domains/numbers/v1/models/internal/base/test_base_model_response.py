from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationResponse


def test_base_model_response_expects_unrecognized_fields_snake_case():
    """
    Expects unrecognized fields to be dynamically added as snake_case attributes.
    """
    data = {
        "unexpectedField": "unexpectedValue",
        "anotherExtraField": 42,
    }
    response = BaseModelConfigurationResponse(**data)

    # Assert unrecognized fields are dynamically added
    assert response.unexpected_field == "unexpectedValue"
    assert response.another_extra_field == 42
