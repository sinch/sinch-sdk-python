from fastapi.testclient import TestClient
from examples.fast_api_example import app, sinch_client


def test_get_available_numbers_get_endpoint(
    auth_origin,
    numbers_origin
):
    sinch_client.configuration.auth_origin = auth_origin
    sinch_client.configuration.numbers_origin = numbers_origin
    sinch_client.configuration.disable_https = True

    client = TestClient(app)
    response = client.get("/available_numbers")
    assert response.status_code == 200
    assert "available_numbers" in response.json()
