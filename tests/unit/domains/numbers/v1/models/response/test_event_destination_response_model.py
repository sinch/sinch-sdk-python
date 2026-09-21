import pytest
from sinch.core.models.internal.base_model_config import transform_kwargs_casing_scope
from sinch.domains.numbers.models.v1.response import EventDestinationResponse


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
    with transform_kwargs_casing_scope(False):
        response = EventDestinationResponse(**test_data)

    assert response.project_id == "project-test-id"
    assert response.hmac_secret == "secret-key-456"
    assert response.extraField == "Extra content"
    assert response.extraDict == {"key": "value"}
