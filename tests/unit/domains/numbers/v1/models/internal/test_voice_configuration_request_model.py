import pytest
from pydantic import TypeAdapter

from sinch.domains.numbers.models.v1.internal import (
    VoiceConfigurationCustom,
    VoiceConfigurationEST,
    VoiceConfigurationFAX,
    VoiceConfigurationRTC,
    VoiceConfigurationRequestUnion,
)

voice_configuration_adapter = TypeAdapter(VoiceConfigurationRequestUnion)


@pytest.mark.parametrize(
    "payload, expected_type, expected_dump",
    [
        (
            {"type": "RTC", "appId": "YOUR_app_id"},
            VoiceConfigurationRTC,
            {"type": "RTC", "appId": "YOUR_app_id"},
        ),
        (
            {"type": "EST", "trunkId": "YOUR_trunk_id"},
            VoiceConfigurationEST,
            {"type": "EST", "trunkId": "YOUR_trunk_id"},
        ),
        (
            {"type": "FAX", "serviceId": "YOUR_service_id"},
            VoiceConfigurationFAX,
            {"type": "FAX", "serviceId": "YOUR_service_id"},
        ),
        (
            {"type": "SOMETHING_NEW", "customField": "abc"},
            VoiceConfigurationCustom,
            {"type": "SOMETHING_NEW", "customField": "abc"},
        ),
        (
            {"appId": "YOUR_app_id"},
            VoiceConfigurationRTC,
            {"type": "RTC", "appId": "YOUR_app_id"},
        ),
        (
            {"type": "", "appId": "YOUR_app_id"},
            VoiceConfigurationRTC,
            {"type": "RTC", "appId": "YOUR_app_id"},
        ),
    ],
    ids=[
        "rtc",
        "est",
        "fax",
        "unknown_type_falls_back_to_custom",
        "missing_type_defaults_to_rtc",
        "empty_type_defaults_to_rtc",
    ],
)
def test_voice_configuration_request_union_resolves_by_type(
    payload, expected_type, expected_dump
):
    """
    Expects each type to resolve to its own request variant, an unrecognized
    type to fall back to VoiceConfigurationCustom, and a missing or empty type
    to default to VoiceConfigurationRTC, all serializing back to the wire shape
    the API expects.
    """
    result = voice_configuration_adapter.validate_python(payload)

    assert type(result) is expected_type
    assert result.model_dump(by_alias=True, exclude_none=True) == expected_dump
