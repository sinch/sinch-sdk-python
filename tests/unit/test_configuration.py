from sinch.core.clients.sinch_client_configuration import Configuration
from sinch.core.adapters.requests_http_transport import HTTPTransportRequests
from sinch.core.token_manager import TokenManager


def test_configuration_initialization_happy_path(sinch_client_sync):
    client_configuration = Configuration(
        key_id="Rodney",
        key_secret="Mullen",
        project_id="Is the King!",
        transport=HTTPTransportRequests(sinch_client_sync),
        token_manager=TokenManager(sinch_client_sync)
    )
    assert client_configuration.key_id == "Rodney"
    assert client_configuration.key_secret == "Mullen"
    assert client_configuration.project_id == "Is the King!"
    assert isinstance(client_configuration.transport, HTTPTransportRequests)
    assert isinstance(client_configuration.token_manager, TokenManager)


def test_set_sms_region_property_and_check_that_sms_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.sms_region = (
        "We interrupt this program to annoy you" 
        "and make things generally more irritating."
    )
    assert "irritating" in sinch_client_sync.configuration.sms_origin


def test_set_sms_region_with_service_plan_id_property_and_check_that_sms_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.sms_region_with_service_plan_id = (
        "Herring"
    )
    assert sinch_client_sync.configuration.sms_origin_with_service_plan_id.startswith("Herring")


def test_set_sms_domain_property_and_check_that_sms_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.sms_domain = (
        "We interrupt this program to annoy you" 
        "and make things generally more irritating."
    )
    assert "irritating" in sinch_client_sync.configuration.sms_origin


def test_set_conversation_region_property_and_check_that_sms_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.conversation_region = "My_brain_hurts!"
    assert "brain" in sinch_client_sync.configuration.conversation_origin
    assert "hurts" in sinch_client_sync.configuration.conversation_origin


def test_set_conversation_domain_property_and_check_that_sms_origin_was_updated(sinch_client_sync):
    sinch_client_sync.configuration.conversation_domain= "My_brain_hurts!"
    assert "brain" in sinch_client_sync.configuration.conversation_origin
    assert "hurts" in sinch_client_sync.configuration.conversation_origin


def test_if_logger_name_was_preserved_correctly(sinch_client_async):
    clever_monty_python_quote = "Its_just_a_flesh_wound"
    client_configuration = Configuration(
        key_id="Do",
        key_secret="a",
        project_id="Kickflip!",
        logger_name=clever_monty_python_quote,
        transport=HTTPTransportRequests(sinch_client_async),
        token_manager=TokenManager(sinch_client_async)
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
