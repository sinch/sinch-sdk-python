from sinch import SinchClient
from sinch.core.clients.sinch_client_configuration import Configuration


def test_sinch_client_initialization():
    """Test that SinchClient can be initialized with or without parameters"""
    sinch_client = SinchClient(key_id="test", key_secret="test_secret", project_id="test_project_id")
    assert sinch_client


def test_sinch_client_expects_all_attributes(sinch_client_sync):
    """Test that SinchClient has all attributes"""
    assert hasattr(sinch_client_sync, "authentication")
    assert hasattr(sinch_client_sync, "sms")
    assert hasattr(sinch_client_sync, "conversation")
    assert hasattr(sinch_client_sync, "numbers")
    assert hasattr(sinch_client_sync, "verification")
    assert hasattr(sinch_client_sync, "voice")
    assert hasattr(sinch_client_sync, "configuration")
    assert isinstance(sinch_client_sync.configuration, Configuration)
