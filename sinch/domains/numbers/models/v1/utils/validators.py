from typing import Dict, Any
from sinch.domains.numbers.models.v1.internal.sms_configuration_request import SmsConfigurationRequest
from sinch.domains.numbers.models.v1.internal.voice_configuration_request import (
    VoiceConfigurationRTC,
    VoiceConfigurationEST,
    VoiceConfigurationFAX,
    VoiceConfigurationCustom,
)
from sinch.domains.numbers.models.v1.shared.number_pattern import NumberPattern


def validate_number_pattern(data: Dict[str, Any]) -> None:
    """
    Validates `number_pattern` field in request data.

    Args:
        data (dict): The request payload.

    Raises:
        ValidationError: If validation fails for the number pattern.
    """
    for key in ("numberPattern", "number_pattern"):
        if key in data and data[key] is not None:
            NumberPattern(**data[key])


def validate_sms_voice_configuration(data: Dict[str, Any]) -> None:
    """
    Validates `sms_configuration` and `voice_configuration` fields in request data.

    Args:
        data (dict): The request payload.

    Raises:
        ValidationError: If validation fails for the configurations.
    """
    # Validate SMS Configuration
    for key in ("smsConfiguration", "sms_configuration"):
        if key in data and data[key] is not None:
            SmsConfigurationRequest(**data[key])

    # Validate Voice Configuration
    voice_config_map = {
        "RTC": VoiceConfigurationRTC,
        "EST": VoiceConfigurationEST,
        "FAX": VoiceConfigurationFAX,
    }

    for key in ("voiceConfiguration", "voice_configuration"):
        if key in data and data[key] is not None:
            # Handle legacy requests
            voice_type = data[key].get("type") or "RTC"
            voice_config_class = voice_config_map.get(voice_type, VoiceConfigurationCustom)
            voice_config_class(**data[key])
