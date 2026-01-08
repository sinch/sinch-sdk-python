import pytest
from sinch import SinchClient
from sinch.core.clients.sinch_client_configuration import Configuration


def test_sinch_client_initialization():
    """ Test that SinchClient can be initialized with or without parameters """
    sinch_client = SinchClient(
        key_id="test",
        key_secret="test_secret",
        project_id="test_project_id"
    )
    assert sinch_client


def test_sinch_client_expects_to_be_initialized_with_sms():
    """ Test that SinchClient can be initialized with sms_region, service_plan_id and sms_api_token """
    sinch_client = SinchClient(
        sms_region="us",
        service_plan_id="test_service_plan",
        sms_api_token="test_sms_token"
    )
    assert sinch_client


def test_sinch_client_expects_all_attributes():
    """ Test that SinchClient has all attributes"""
    sinch_client = SinchClient(
        key_id="test_key_id",
        key_secret="test_key_secret",
        project_id="test_project_id"
    )
    
    assert hasattr(sinch_client, "authentication")
    assert hasattr(sinch_client, "sms")
    assert hasattr(sinch_client, "conversation")
    assert hasattr(sinch_client, "numbers")
    assert hasattr(sinch_client, "verification")
    assert hasattr(sinch_client, "voice")
    assert hasattr(sinch_client, "configuration")
    assert isinstance(sinch_client.configuration, Configuration)


def test_sinch_client_expects_to_be_initialized_with_conversation_region():
    """ Test that SinchClient can be initialized with conversation_region """
    sinch_client = SinchClient(
        key_id="test_key_id",
        key_secret="test_key_secret",
        project_id="test_project_id",
        conversation_region="eu"
    )
    assert sinch_client.configuration.conversation_region == "eu"
    assert sinch_client.configuration.conversation_origin == "https://eu.conversation.api.sinch.com/"


def test_sinch_client_expects_conversation_region_error_when_not_provided():
    """ Test that get_conversation_origin raises ValueError when SinchClient is initialized without conversation_region """
    sinch_client = SinchClient(
        key_id="test_key_id",
        key_secret="test_key_secret",
        project_id="test_project_id"
    )
    
    assert sinch_client.configuration.conversation_region is None
    assert sinch_client.configuration.conversation_origin is None
    
    with pytest.raises(ValueError, match="Conversation region is required"):
        sinch_client.configuration.get_conversation_origin()
