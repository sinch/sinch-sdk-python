import threading

import pytest
from sinch import SinchClient
from sinch.core.clients.sinch_client_configuration import Configuration
from sinch.core.models.internal.base_model_config import (
    _legacy_extra_fields_normalization,
    legacy_extra_fields_normalization_scope,
)


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
    assert hasattr(sinch_client, "number_lookup")
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
    assert sinch_client.configuration.conversation_origin == "https://eu.conversation.api.sinch.com"


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


class TestLegacyExtraFieldsNormalizationIsolation:
    """`legacy_extra_fields_normalization` is per-client: each Configuration
    holds its own value, and the request-scoped ContextVar that drives model
    normalization
    """

    def test_two_configurations_hold_independent_values(self):
        client_a = SinchClient(project_id="project_a", legacy_extra_fields_normalization=False)
        client_b = SinchClient(project_id="project_b", legacy_extra_fields_normalization=True)

        assert client_a.configuration.legacy_extra_fields_normalization is False
        assert client_b.configuration.legacy_extra_fields_normalization is True

    def test_sequential_use_on_same_thread_does_not_leak(self):
        client_a = SinchClient(project_id="project_a", legacy_extra_fields_normalization=False)
        client_b = SinchClient(project_id="project_b", legacy_extra_fields_normalization=True)

        with legacy_extra_fields_normalization_scope(
            client_b.configuration.legacy_extra_fields_normalization
        ):
            assert _legacy_extra_fields_normalization.get() is True

        with legacy_extra_fields_normalization_scope(
            client_a.configuration.legacy_extra_fields_normalization
        ):
            assert _legacy_extra_fields_normalization.get() is False

    def test_concurrent_use_on_different_threads_does_not_leak(self):
        client_a = SinchClient(project_id="project_a", legacy_extra_fields_normalization=False)
        client_b = SinchClient(project_id="project_b", legacy_extra_fields_normalization=True)
        results = {}
        barrier = threading.Barrier(2)

        def call_as(name, client):
            with legacy_extra_fields_normalization_scope(
                client.configuration.legacy_extra_fields_normalization
            ):
                barrier.wait()
                results[name] = _legacy_extra_fields_normalization.get()

        thread_a = threading.Thread(target=call_as, args=("a", client_a))
        thread_b = threading.Thread(target=call_as, args=("b", client_b))
        thread_a.start()
        thread_b.start()
        thread_a.join()
        thread_b.join()

        assert results["a"] is False
        assert results["b"] is True