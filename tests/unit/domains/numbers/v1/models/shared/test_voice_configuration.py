from datetime import datetime, timezone

import pytest
from pydantic import TypeAdapter

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.domains.numbers.models.v1.shared import VoiceConfiguration
from sinch.domains.numbers.models.v1.shared.voice_configuration_custom import (
    VoiceConfigurationCustom,
)
from sinch.domains.numbers.models.v1.shared.voice_configuration_est import (
    VoiceConfigurationEST,
)
from sinch.domains.numbers.models.v1.shared.voice_configuration_fax import (
    VoiceConfigurationFAX,
)
from sinch.domains.numbers.models.v1.shared.voice_configuration_rtc import (
    VoiceConfigurationRTC,
)

adapter = TypeAdapter(VoiceConfiguration)

LAST_UPDATED = "2025-01-24T09:32:27.437Z"
LAST_UPDATED_UTC = datetime(2025, 1, 24, 9, 32, 27, 437000, tzinfo=timezone.utc)


@pytest.mark.parametrize(
    "payload, expected_type, expected_fields",
    [
        (
            {
                "type": "RTC",
                "appId": "test_app",
                "lastUpdatedTime": LAST_UPDATED,
                "scheduledVoiceProvisioning": {
                    "type": "EST",
                    "lastUpdatedTime": LAST_UPDATED,
                    "status": "WAITING",
                    "trunkId": "test_app_est",
                },
            },
            VoiceConfigurationRTC,
            {"app_id": "test_app", "last_updated_time": LAST_UPDATED_UTC},
        ),
        (
            {
                "type": "EST",
                "trunkId": "test_trunk",
                "lastUpdatedTime": LAST_UPDATED,
            },
            VoiceConfigurationEST,
            {"trunk_id": "test_trunk", "last_updated_time": LAST_UPDATED_UTC},
        ),
        (
            {
                "type": "FAX",
                "serviceId": "test_service",
                "lastUpdatedTime": LAST_UPDATED,
            },
            VoiceConfigurationFAX,
            {
                "service_id": "test_service",
                "last_updated_time": LAST_UPDATED_UTC,
            },
        ),
        (
            {"type": "SOMETHING_NEW", "customField": "custom_value"},
            VoiceConfigurationCustom,
            {"type": "SOMETHING_NEW"},
        ),
        (
            {"appId": "test_app"},
            VoiceConfigurationRTC,
            {"app_id": "test_app"},
        ),
    ],
    ids=["rtc", "est", "fax", "unknown_type", "missing_type"],
)
def test_voice_configuration_resolves_by_type(
    payload, expected_type, expected_fields
):
    """
    Expects each type to resolve to its own response variant, an unrecognized
    type to fall back to VoiceConfigurationCustom so a configuration added to
    the API later stays parseable, and a payload without a type to resolve by
    its fields, as the spec defaults the type to RTC.
    """
    with response_parsing_scope():
        config = adapter.validate_python(payload)

    assert type(config) is expected_type
    for name, value in expected_fields.items():
        assert getattr(config, name) == value


def test_voice_configuration_resolves_its_nested_scheduled_provisioning():
    """
    Expects the nested scheduledVoiceProvisioning union to resolve on its own,
    independently of the variant carrying it.
    """
    payload = {
        "type": "RTC",
        "appId": "test_app",
        "scheduledVoiceProvisioning": {
            "type": "EST",
            "status": "WAITING",
            "trunkId": "test_app_est",
        },
    }
    with response_parsing_scope():
        config = adapter.validate_python(payload)

    assert config.scheduled_voice_provisioning.type == "EST"
    assert config.scheduled_voice_provisioning.trunk_id == "test_app_est"
    assert config.scheduled_voice_provisioning.status == "WAITING"

