from sinch import SinchClient, SinchClientAsync
from sinch.core.clients.sinch_client_configuration import Configuration


def test_sinch_client_initialization():
    sinch_client_sync = SinchClient(
        key_id="test",
        key_secret="test_secret",
        project_id="test_project_id"
    )
    assert sinch_client_sync


def test_sinch_client_async_initialization():
    sinch_client_async = SinchClientAsync(
        key_id="test",
        key_secret="test_secret",
        project_id="test_project_id"
    )
    assert sinch_client_async


def test_sinch_client_has_all_business_domains(sinch_client_sync):
    assert hasattr(sinch_client_sync, "authentication")
    assert hasattr(sinch_client_sync, "sms")
    assert hasattr(sinch_client_sync, "conversation")
    assert hasattr(sinch_client_sync, "numbers")


def test_sinch_client_async_has_all_business_domains(sinch_client_async):
    assert hasattr(sinch_client_async, "authentication")
    assert hasattr(sinch_client_async, "sms")
    assert hasattr(sinch_client_async, "conversation")
    assert hasattr(sinch_client_async, "numbers")


def test_sinch_client_has_configuration_object(sinch_client_sync):
    assert hasattr(sinch_client_sync, "configuration")
    assert isinstance(sinch_client_sync.configuration, Configuration)


def test_sinch_client_async_has_configuration_object(sinch_client_async):
    assert hasattr(sinch_client_async, "configuration")
    assert isinstance(sinch_client_async.configuration, Configuration)
