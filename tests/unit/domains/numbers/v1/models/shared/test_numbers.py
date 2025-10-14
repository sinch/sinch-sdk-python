from datetime import datetime, timezone
from pydantic import TypeAdapter
from sinch.domains.numbers.models.v1.shared import ScheduledSmsProvisioning, SmsConfiguration
from sinch.domains.numbers.models.v1.types import VoiceConfiguration


def test_scheduled_provisioning_sms_configuration_valid_expects_parsed_data():
    """
    Test a valid instance of ScheduledProvisioningSmsConfiguration
    """
    data = {
        "servicePlanId": "test_plan",
        "campaignId": "test_campaign",
        "status": "ACTIVE",
        "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
        "errorCodes": ["ERROR_CODE_1"],
    }
    config = ScheduledSmsProvisioning.model_validate(data)

    assert config.service_plan_id == "test_plan"
    assert config.campaign_id == "test_campaign"
    assert config.status == "ACTIVE"
    expected_last_updated_time = datetime(2025, 1, 24, 9, 32, 27, 437000, tzinfo=timezone.utc)
    assert config.last_updated_time == expected_last_updated_time
    assert config.error_codes == ["ERROR_CODE_1"]


def test_scheduled_provisioning_sms_configuration_optional_fields_expects_parsed_data():
    """
    Test missing optional fields in ScheduledProvisioningSmsConfiguration
    """
    data = {"servicePlanId": "test_plan"}
    config = ScheduledSmsProvisioning.model_validate(data)

    assert config.service_plan_id == "test_plan"
    assert config.campaign_id is None
    assert config.status is None
    assert config.last_updated_time is None
    assert config.error_codes is None


def test_sms_configuration_valid_expects_parsed_data():
    """
    Test a valid instance of SmsConfiguration
    """
    data = {
        "servicePlanId": "test_plan",
        "campaignId": "test_campaign",
        "scheduledProvisioning": {"servicePlanId": "test_plan", "status": "ACTIVE"},
    }
    config = SmsConfiguration.model_validate(data)

    assert config.service_plan_id == "test_plan"
    assert config.campaign_id == "test_campaign"
    assert config.scheduled_provisioning is not None
    assert config.scheduled_provisioning.service_plan_id == "test_plan"
    assert config.scheduled_provisioning.status == "ACTIVE"


def test_voice_configuration_rtc_valid_expects_parsed_data():
    """
    Test a valid RTC voice configuration
    """
    data = {
        "type": "RTC",
        "appId": "test_app",
        "trunkId": "",
        "serviceId": "",
        "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
        "scheduledVoiceProvisioning": {
            "type": "EST",
            "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
            "status": "WAITING",
            "appId": "",
            "trunkId": "test_app_est",
            "serviceId": "",
        },
    }

    voice_configuration_adapter = TypeAdapter(VoiceConfiguration)
    config = voice_configuration_adapter.validate_python(data)

    assert config.type == "RTC"
    assert config.app_id == "test_app"
    assert config.last_updated_time == datetime(2025, 1, 24, 9, 32, 27, 437000, tzinfo=timezone.utc)
    assert config.scheduled_voice_provisioning is not None
    assert config.scheduled_voice_provisioning.type == "EST"
    assert config.scheduled_voice_provisioning.status == "WAITING"
    assert config.scheduled_voice_provisioning.trunk_id == "test_app_est"


def test_voice_configuration_est_valid_expects_parsed_data():
    """
    Test a valid EST voice configuration
    """
    data = {
        "type": "EST",
        "appId": "",
        "trunkId": "test_trunk",
        "serviceId": "",
        "lastUpdatedTime": "2025-02-25T09:32:27.437Z",
        "scheduledVoiceProvisioning": {
            "type": "EST",
            "lastUpdatedTime": "2025-02-25T09:32:27.437Z",
            "status": "ACTIVE",
            "appId": "",
            "trunkId": "test_trunk",
            "serviceId": "",
        },
    }

    voice_configuration_adapter = TypeAdapter(VoiceConfiguration)
    config = voice_configuration_adapter.validate_python(data)

    assert config.type == "EST"
    assert config.trunk_id == "test_trunk"
    assert config.last_updated_time == datetime(2025, 2, 25, 9, 32, 27, 437000, tzinfo=timezone.utc)
    assert config.scheduled_voice_provisioning is not None
    assert config.scheduled_voice_provisioning.type == "EST"
    assert config.scheduled_voice_provisioning.trunk_id == "test_trunk"
    assert config.scheduled_voice_provisioning.status == "ACTIVE"


def test_voice_configuration_fax_valid_expects_parsed_data():
    """
    Test a valid FAX voice configuration
    """
    data = {
        "type": "FAX",
        "appId": "",
        "trunkId": "",
        "serviceId": "test_service",
        "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
        "scheduledVoiceProvisioning": {
            "type": "FAX",
            "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
            "status": "ACTIVE",
            "appId": "",
            "trunkId": "",
            "serviceId": "test_service",
        },
    }

    voice_configuration_adapter = TypeAdapter(VoiceConfiguration)
    config = voice_configuration_adapter.validate_python(data)

    assert config.type == "FAX"
    assert config.service_id == "test_service"
    assert config.last_updated_time == datetime(2025, 1, 24, 9, 32, 27, 437000, tzinfo=timezone.utc)
    assert config.scheduled_voice_provisioning is not None
    assert config.scheduled_voice_provisioning.type == "FAX"
    assert config.scheduled_voice_provisioning.status == "ACTIVE"
    assert config.scheduled_voice_provisioning.service_id == "test_service"
