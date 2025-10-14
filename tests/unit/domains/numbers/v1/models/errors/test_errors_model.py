from sinch.domains.numbers.models.v1.errors import NotFoundError


def test_not_found_error_deserialize_with_snake_case():
    data = {
        "code": 404,
        "message": "",
        "status": "NOT_FOUND",
        "details": [
            {
                "type": "ResourceInfo",
                "resourceType": "AvailableNumber",
                "resourceName": "+1234567890",
                "owner": "",
                "description": "",
            }
        ],
    }

    not_found_error = NotFoundError.model_validate(data)

    assert not_found_error.code == 404
    assert not_found_error.message == ""
    assert not_found_error.status == "NOT_FOUND"
    assert not_found_error.details[0].type == "ResourceInfo"
    assert not_found_error.details[0].resource_type == "AvailableNumber"
    assert not_found_error.details[0].resource_name == "+1234567890"
    assert not_found_error.details[0].owner == ""
    assert not_found_error.details[0].description == ""
