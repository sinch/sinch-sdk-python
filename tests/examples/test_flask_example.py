from examples.flask_example import app, sinch_client


def test_flask_create_app_get_endpoint(
    auth_origin,
    conversation_origin
):
    sinch_client.configuration.auth_origin = auth_origin
    sinch_client.configuration.conversation_origin = conversation_origin
    sinch_client.configuration.disable_https = True
    app.testing = True
    flask_client = app.test_client()

    response = flask_client.post("/create_app")
    assert response.status_code == 200
    assert "sinch_app_id" in response.json
