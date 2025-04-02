import pytest
from sinch.domains.numbers.models.v1.response import CallbackConfigurationResponse


@pytest.fixture
def test_data():
    return {
        "projectId": "project-test-id",
        "hmacSecret": "secret-key-456",
        "extraField": "Extra content",
        "extraDict": {"key": "value"}
    }


def test_numbers_callback_config_response_all_fields(test_data):
    """
    Expects all fields to map correctly from camelCase input
    and handle extra fields appropriately
    """
    response = CallbackConfigurationResponse(**test_data)

    assert response.project_id == "project-test-id"
    assert response.hmac_secret == "secret-key-456"
    assert response.extra_field == "Extra content"
    assert response.extra_dict == {"key": "value"}
