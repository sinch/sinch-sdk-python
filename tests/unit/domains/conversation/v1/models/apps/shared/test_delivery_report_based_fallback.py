import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.apps.shared.delivery_report_based_fallback import (
    DeliveryReportBasedFallback,
)


def test_delivery_report_based_fallback_expects_parsed_input():
    """Test that the model correctly parses a full valid input."""
    model = DeliveryReportBasedFallback(
        enabled=True,
        delivery_report_waiting_time=60,
    )

    assert model.enabled is True
    assert model.delivery_report_waiting_time == 60


def test_delivery_report_based_fallback_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = DeliveryReportBasedFallback()

    assert model.enabled is None
    assert model.delivery_report_waiting_time is None