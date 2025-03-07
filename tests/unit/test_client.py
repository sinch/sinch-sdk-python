import pytest
from sinch import SinchClient, SinchClientAsync
from sinch.core.clients.sinch_client_configuration import Configuration

@pytest.mark.parametrize("client", [SinchClient, SinchClientAsync])
def test_sinch_client_initialization(client):
    """ Test that SinchClient and SinchClientAsync can be initialized with or without parameters """
    sinch_client = client(
        key_id="test",
        key_secret="test_secret",
        project_id="test_project_id"
    )
    assert sinch_client

    sinch_client_empty = client()
    assert sinch_client_empty


@pytest.mark.parametrize("client", ["sinch_client_sync", "sinch_client_async"])
def test_sinch_client_expects_all_attributes(request, client):
    """ Test that SinchClient and SinchClientAsync have all attributes"""
    client_instance = request.getfixturevalue(client)
    assert hasattr(client_instance, "authentication")
    assert hasattr(client_instance, "sms")
    assert hasattr(client_instance, "conversation")
    assert hasattr(client_instance, "numbers")
    assert hasattr(client_instance, "verification")
    assert hasattr(client_instance, "voice")
    assert hasattr(client_instance, "configuration")
    assert isinstance(client_instance.configuration, Configuration)
