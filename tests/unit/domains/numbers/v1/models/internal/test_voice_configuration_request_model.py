from pydantic import TypeAdapter
from sinch.domains.numbers.models.v1.internal import (
    VoiceConfigurationCustom,
    VoiceConfigurationEST,
    VoiceConfigurationFAX,
    VoiceConfigurationRTC,
    VoiceConfigurationRequestUnion,
)

voice_configuration_adapter = TypeAdapter(VoiceConfigurationRequestUnion)


def test_voice_configuration_request_union_expects_rtc_parsed():
    """
    Test that a RTC payload parses into VoiceConfigurationRTC.
    """
    result = voice_configuration_adapter.validate_python(
        {"type": "RTC", "appId": "YOUR_app_id"}
    )
    assert isinstance(result, VoiceConfigurationRTC)
    assert result.type == "RTC"
    assert result.app_id == "YOUR_app_id"
    assert result.model_dump(by_alias=True, exclude_none=True) == {
        "type": "RTC",
        "appId": "YOUR_app_id",
    }


def test_voice_configuration_request_union_expects_est_parsed():
    """
    Test that an EST payload parses into VoiceConfigurationEST.
    """
    result = voice_configuration_adapter.validate_python(
        {"type": "EST", "trunkId": "YOUR_trunk_id"}
    )
    assert isinstance(result, VoiceConfigurationEST)
    assert result.type == "EST"
    assert result.trunk_id == "YOUR_trunk_id"
    assert result.model_dump(by_alias=True, exclude_none=True) == {
        "type": "EST",
        "trunkId": "YOUR_trunk_id",
    }


def test_voice_configuration_request_union_expects_fax_parsed():
    """
    Test that a FAX payload parses into VoiceConfigurationFAX.
    """
    result = voice_configuration_adapter.validate_python(
        {"type": "FAX", "serviceId": "YOUR_service_id"}
    )
    assert isinstance(result, VoiceConfigurationFAX)
    assert result.type == "FAX"
    assert result.service_id == "YOUR_service_id"
    assert result.model_dump(by_alias=True, exclude_none=True) == {
        "type": "FAX",
        "serviceId": "YOUR_service_id",
    }


def test_voice_configuration_request_union_expects_custom_parsed():
    """
    Test that an unrecognized type parses into VoiceConfigurationCustom.
    """
    result = voice_configuration_adapter.validate_python(
        {"type": "SOMETHING_NEW", "customField": "abc"}
    )
    assert isinstance(result, VoiceConfigurationCustom)
    assert result.type == "SOMETHING_NEW"
    assert result.model_dump(by_alias=True, exclude_none=True) == {
        "type": "SOMETHING_NEW",
        "customField": "abc",
    }


def test_voice_configuration_request_union_expects_missing_type_defaults_to_rtc():
    """
    Test that a payload without `type` defaults to VoiceConfigurationRTC.
    """
    result = voice_configuration_adapter.validate_python({"appId": "YOUR_app_id"})
    assert isinstance(result, VoiceConfigurationRTC)
    assert result.type == "RTC"
    assert result.app_id == "YOUR_app_id"


def test_voice_configuration_request_union_expects_empty_type_defaults_to_rtc():
    """
    Test that a payload with an empty `type` string defaults to VoiceConfigurationRTC.
    """
    result = voice_configuration_adapter.validate_python(
        {"type": "", "appId": "YOUR_app_id"}
    )
    assert isinstance(result, VoiceConfigurationRTC)
    assert result.type == "RTC"
    assert result.app_id == "YOUR_app_id"
