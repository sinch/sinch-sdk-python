import pytest
from datetime import datetime, timezone

@pytest.fixture
def test_data():
    return {
        "phoneNumber": "+12025550134",
        "displayName": "string",
        "regionCode": "US",
        "type": "MOBILE",
        "capability": ["SMS"],
        "money": {"currencyCode": "USD", "amount": "2.00"},
        "paymentIntervalMonths": 0,
        "nextChargeDate": "2025-01-22T13:19:31.095Z",
        "expireAt": "2025-02-04T13:15:31.095Z",
        "smsConfiguration": {
            "servicePlanId": "string",
            "campaignId": "string",
            "scheduledProvisioning": {
                "servicePlanId": "string",
                "campaignId": "string",
                "status": "PROVISIONING_STATUS_UNSPECIFIED",
                "lastUpdatedTime": "2025-01-24T13:19:31.095Z",
                "errorCodes": ["ERROR_CODE_UNSPECIFIED"],
            },
        },
        "voiceConfiguration": {
            "lastUpdatedTime": "2025-01-25T18:19:31.095Z",
            "scheduledVoiceProvisioning": {
                "type": "RTC",
                "lastUpdatedTime": "2025-01-26T18:19:31.095Z",
                "status": "PROVISIONING_STATUS_UNSPECIFIED",
                "trunkId": "string",
            },
            "appId": "string",
        },
        "callbackUrl": "https://www.your-callback-server.com/callback",
    }

def assert_sms_configuration(sms_config):
    """
    Assert sms_configuration fields.
    """
    assert sms_config.service_plan_id == "string"
    assert sms_config.campaign_id == "string"
    scheduled_provisioning = sms_config.scheduled_provisioning
    assert scheduled_provisioning.service_plan_id == "string"
    assert scheduled_provisioning.campaign_id == "string"
    assert scheduled_provisioning.status == "PROVISIONING_STATUS_UNSPECIFIED"
    expected_last_updated_time = (
        datetime(2025, 2, 21, 13, 19, 31, 95000, tzinfo=timezone.utc))
    assert scheduled_provisioning.last_updated_time == expected_last_updated_time
    assert scheduled_provisioning.error_codes == ["ERROR_CODE_UNSPECIFIED"]

def assert_voice_configuration(voice_config):
    """
    Assert voice_configuration fields.
    """
    assert voice_config.type == "RTC"
    expected_last_updated_time = (
        datetime(2025, 1, 25, 13, 49, 31, 95000, tzinfo=timezone.utc))
    assert voice_config.last_updated_time == expected_last_updated_time
    assert voice_config.app_id == "string"
    scheduled_voice_provisioning = voice_config.scheduled_voice_provisioning
    assert scheduled_voice_provisioning.type == "RTC"
    expected_last_updated_time = (
        datetime(2025, 2, 22, 13, 19, 31, 95000, tzinfo=timezone.utc))
    assert scheduled_voice_provisioning.last_updated_time == expected_last_updated_time
    assert scheduled_voice_provisioning.status == "PROVISIONING_STATUS_UNSPECIFIED"
    assert scheduled_voice_provisioning.app_id == "string"
