from logging import Logger, getLogger
import pytest
from sinch.core.clients.sinch_client_configuration import Configuration
from sinch.core.adapters.requests_http_transport import HTTPTransportRequests
from sinch.core.token_manager import TokenManager


def test_configuration_happy_capy_expects_initialization(sinch_client_sync):
    """ Test that Configuration can be initialized with all parameters """
    client_configuration = Configuration(
        transport=HTTPTransportRequests(sinch_client_sync),
        token_manager=TokenManager(sinch_client_sync),
        key_id="CapyKey",
        key_secret="CapybaraWhisper",
        project_id="CapybaraProjectX",
        logger=getLogger("CapyTrace"),
        connection_timeout=10,
        application_key="AppybaraKey",
        application_secret="SecretHabitatEntry",
        service_plan_id="CappyPremiumPlan",
        sms_api_token="HappyCappyToken",
        sms_region="us"
    )

    assert client_configuration.key_id == "CapyKey"
    assert client_configuration.key_secret == "CapybaraWhisper"
    assert client_configuration.project_id == "CapybaraProjectX"
    assert isinstance(client_configuration.logger, Logger)
    assert client_configuration.application_key == "AppybaraKey"
    assert client_configuration.application_secret == "SecretHabitatEntry"
    assert client_configuration.service_plan_id == "CappyPremiumPlan"
    assert client_configuration.sms_api_token == "HappyCappyToken"
    assert client_configuration.sms_region == "us"
    assert isinstance(client_configuration.transport, HTTPTransportRequests)
    assert isinstance(client_configuration.token_manager, TokenManager)


def test_set_sms_region_property_and_check_that_sms_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.sms_region = "pl"
    assert "https://zt.pl.sms.api.sinch.com" == sinch_client_sync.configuration.sms_origin


def test_configuration_expects_set_sms_domain_property_and_check_that_sms_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.sms_region = "us"
    sinch_client_sync.configuration.sms_domain = "{}.monty.python"
    assert "us.monty.python" == sinch_client_sync.configuration.sms_origin


def test_set_sms_region_with_service_plan_id_property_and_check_that_sms_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.sms_region_with_service_plan_id = "Herring"
    assert sinch_client_sync.configuration.sms_origin_with_service_plan_id == "https://Herring.sms.api.sinch.com"


def test_set_conversation_region_property_and_check_that_sms_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.conversation_region = "My_brain_hurts"
    assert "brain" in sinch_client_sync.configuration.conversation_origin
    assert "hurts" in sinch_client_sync.configuration.conversation_origin


def test_set_conversation_domain_property_and_check_that_sms_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.conversation_domain = "My_brain_hurts"
    assert "brain" in sinch_client_sync.configuration.conversation_origin
    assert "hurts" in sinch_client_sync.configuration.conversation_origin


def test_if_logger_name_was_preserved_correctly(sinch_client_sync):
    clever_monty_python_quote = "Its_just_a_flesh_wound"
    client_configuration = Configuration(
        transport=HTTPTransportRequests(sinch_client_sync),
        token_manager=TokenManager(sinch_client_sync),
        key_id="Do",
        key_secret="a",
        project_id="Kickflip!",
        logger_name=clever_monty_python_quote,
    )
    client_configuration.logger.name = clever_monty_python_quote
    assert client_configuration.logger.name == clever_monty_python_quote


def test_set_templates_region_property_and_check_that_templates_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.templates_region = "Are_you_suggesting_that_coconuts_migrate?"
    assert "coconuts" in sinch_client_sync.configuration.templates_origin
    assert "migrate" in sinch_client_sync.configuration.templates_origin


def test_set_templates_domain_property_and_check_that_templates_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.templates_domain = "Are_you_suggesting_that_coconuts_migrate?"
    assert "coconuts" in sinch_client_sync.configuration.templates_origin
    assert "migrate" in sinch_client_sync.configuration.templates_origin


def test_configuration_expects_authentication_method_determination_sms_auth_priority(sinch_client_sync):
    """ Test that SMS authentication takes priority over project authentication """
    client_configuration = Configuration(
        transport=HTTPTransportRequests(sinch_client_sync),
        token_manager=TokenManager(sinch_client_sync),
        service_plan_id="test_service_plan",
        sms_api_token="test_sms_token",
        project_id="test_project_id"
    )
    
    assert client_configuration.authentication_method == "sms_auth"


def test_configuration_expects_authentication_method_determination_project_auth_fallback(sinch_client_sync):
    """ Test that project authentication is used when SMS auth parameters are not provided """
    client_configuration = Configuration(
        transport=HTTPTransportRequests(sinch_client_sync),
        token_manager=TokenManager(sinch_client_sync),
        project_id="test_project_id",
        key_id="test_key_id",
        key_secret="test_key_secret"
    )
    
    assert client_configuration.authentication_method == "project_auth"


def test_configuration_expects_sms_authentication_method_setting_sms_auth(sinch_client_sync):
    """ Test that SMS authentication method is set to SMS_TOKEN for SMS auth """
    client_configuration = Configuration(
        transport=HTTPTransportRequests(sinch_client_sync),
        token_manager=TokenManager(sinch_client_sync),
        service_plan_id="test_service_plan",
        sms_api_token="test_sms_token"
    )
    
    assert client_configuration.authentication_method == "sms_auth"


def test_configuration_expects_authentication_method_determination_insufficient_parameters(sinch_client_sync):
    """ Test that insufficient authentication parameters raise an error when validated """
    client_configuration = Configuration(
        transport=HTTPTransportRequests(sinch_client_sync),
        token_manager=TokenManager(sinch_client_sync)
    )
    
    assert client_configuration.authentication_method is None
    
    with pytest.raises(ValueError, match="Project authentication requires 'project_id'"):
        client_configuration.validate_authentication_parameters()


def test_configuration_expects_authentication_method_determination_only_service_plan_id(sinch_client_sync):
    """ Test that only service_plan_id without sms_api_token is None """
    client_configuration = Configuration(
        transport=HTTPTransportRequests(sinch_client_sync),
        token_manager=TokenManager(sinch_client_sync),
        service_plan_id="test_service_plan"
    )
    
    assert client_configuration.authentication_method is None
    
    with pytest.raises(ValueError, match="Project authentication requires 'project_id'"):
        client_configuration.validate_authentication_parameters()


def test_configuration_expects_sms_origin_for_auth_sms_authentication(sinch_client_sync):
    """ Test that SMS authentication returns sms_origin_with_service_plan_id """
    client_configuration = Configuration(
        transport=HTTPTransportRequests(sinch_client_sync),
        token_manager=TokenManager(sinch_client_sync),
        service_plan_id="test_service_plan",
        sms_api_token="test_sms_token",
        sms_region="us"
    )
    
    expected_origin = client_configuration.sms_origin_with_service_plan_id
    actual_origin = client_configuration.get_sms_origin_for_auth()
    
    assert actual_origin == expected_origin
    assert actual_origin == "https://us.sms.api.sinch.com"


def test_configuration_expects_get_sms_origin_for_auth_project_authentication(sinch_client_sync):
    """ Test that project authentication returns regular sms_origin """
    client_configuration = Configuration(
        transport=HTTPTransportRequests(sinch_client_sync),
        token_manager=TokenManager(sinch_client_sync),
        project_id="test_project_id",
        sms_region="eu"
    )
    
    expected_origin = client_configuration.sms_origin
    actual_origin = client_configuration.get_sms_origin_for_auth()
    
    assert actual_origin == expected_origin
    assert actual_origin == "https://zt.eu.sms.api.sinch.com"
