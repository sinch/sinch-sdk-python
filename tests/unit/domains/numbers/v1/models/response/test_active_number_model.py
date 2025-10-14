from datetime import datetime, timezone
import pytest
from sinch.domains.numbers.models.v1.response import ActiveNumber


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
            "type": "EST",
            "lastUpdatedTime": "2025-01-25T18:19:31.095Z",
            "scheduledVoiceProvisioning": {
                "type": "EST",
                "lastUpdatedTime": "2025-01-26T18:19:31.095Z",
                "status": "PROVISIONING_STATUS_UNSPECIFIED",
                "trunkId": "string",
            },
            "appId": "string",
        },
        "callbackUrl": "https://www.your-callback-server.com/callback",
        "extraField": "Extra content",
        "extraDict": {"key": "value"},
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
    expected_last_updated_time = datetime(2025, 1, 24, 13, 19, 31, 95000, tzinfo=timezone.utc)
    assert scheduled_provisioning.last_updated_time == expected_last_updated_time
    assert scheduled_provisioning.error_codes == ["ERROR_CODE_UNSPECIFIED"]


def assert_voice_configuration(voice_config):
    """
    Assert voice_configuration fields.
    """
    assert voice_config.type == "EST"
    expected_last_updated_time = datetime(2025, 1, 25, 18, 19, 31, 95000, tzinfo=timezone.utc)
    assert voice_config.last_updated_time == expected_last_updated_time
    assert voice_config.app_id == "string"
    scheduled_voice_provisioning = voice_config.scheduled_voice_provisioning
    assert scheduled_voice_provisioning.type == "EST"
    expected_last_updated_time = datetime(2025, 1, 26, 18, 19, 31, 95000, tzinfo=timezone.utc)
    assert scheduled_voice_provisioning.last_updated_time == expected_last_updated_time
    assert scheduled_voice_provisioning.status == "PROVISIONING_STATUS_UNSPECIFIED"
    assert scheduled_voice_provisioning.trunk_id == "string"


def test_active_number_response_expects_all_fields_mapped_correctly(test_data):
    """
    Expects all fields to map correctly from camelCase input,
    converts nested keys to snake_case, and handles dynamic fields
    """

    response = ActiveNumber(**test_data)

    assert response.phone_number == "+12025550134"
    assert response.display_name == "string"
    assert response.region_code == "US"
    assert response.type == "MOBILE"
    assert response.capability == ["SMS"]
    assert response.money.currency_code == "USD"
    assert response.payment_interval_months == 0
    expected_next_charge_data = datetime(2025, 1, 22, 13, 19, 31, 95000, tzinfo=timezone.utc)
    assert response.next_charge_date == expected_next_charge_data
    expected_expire_at = datetime(2025, 2, 4, 13, 15, 31, 95000, tzinfo=timezone.utc)
    assert response.expire_at == expected_expire_at
    assert response.callback_url == "https://www.your-callback-server.com/callback"

    assert_sms_configuration(response.sms_configuration)
    assert_voice_configuration(response.voice_configuration)

    assert response.extra_field == "Extra content"
    assert response.extra_dict == {"key": "value"}
