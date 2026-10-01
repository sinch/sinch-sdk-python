from datetime import datetime, timezone
from sinch.domains.numbers.models.v1.shared import ScheduledSmsProvisioning, SmsConfiguration

def test_scheduled_provisioning_sms_configuration_valid_expects_parsed_data():
    """
    Test a valid instance of ScheduledProvisioningSmsConfiguration
    """
    data = {
        "servicePlanId": "test_plan",
        "campaignId": "test_campaign",
        "status": "ACTIVE",
        "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
        "errorCodes": ["ERROR_CODE_1"]
    }
    config = ScheduledSmsProvisioning.model_validate(data)

    assert config.service_plan_id == "test_plan"
    assert config.campaign_id == "test_campaign"
    assert config.status == "ACTIVE"
    expected_last_updated_time = (
        datetime(2025, 1, 24, 9, 32, 27, 437000, tzinfo=timezone.utc))
    assert config.last_updated_time == expected_last_updated_time
    assert config.error_codes == ["ERROR_CODE_1"]


def test_scheduled_provisioning_sms_configuration_optional_fields_expects_parsed_data():
    """
    Test missing optional fields in ScheduledProvisioningSmsConfiguration
    """
    data = {
        "servicePlanId": "test_plan"
    }
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
        "scheduledProvisioning": {
            "servicePlanId": "test_plan",
            "status": "ACTIVE"
        }
    }
    config = SmsConfiguration.model_validate(data)

    assert config.service_plan_id == "test_plan"
    assert config.campaign_id == "test_campaign"
    assert config.scheduled_provisioning is not None
    assert config.scheduled_provisioning.service_plan_id == "test_plan"
    assert config.scheduled_provisioning.status == "ACTIVE"
