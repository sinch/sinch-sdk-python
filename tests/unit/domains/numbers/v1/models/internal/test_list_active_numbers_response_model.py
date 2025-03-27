from datetime import datetime, timezone
from decimal import Decimal
import pytest
from sinch.domains.numbers.models.v1.internal import ListActiveNumbersResponse


@pytest.fixture
def test_data():
    return {
        "activeNumbers": [
            {
                "phoneNumber": "+12085088605",
                "projectId": "37b62a7b-0177-429a-bb0b-e10f848de0b8",
                "displayName": "",
                "regionCode": "US",
                "type": "LOCAL",
                "capability": [
                    "SMS",
                    "VOICE"
                ],
                "money": {
                    "currencyCode": "EUR",
                    "amount": "0.80"
                },
                "paymentIntervalMonths": 1,
                "nextChargeDate": "2025-03-04T15:28:16.449951Z",
                "expireAt": None,
                "smsConfiguration": {
                    "servicePlanId": "al_2308",
                    "scheduledProvisioning": None,
                    "campaignId": ""
                },
                "voiceConfiguration": {
                    "appId": "",
                    "scheduledVoiceProvisioning": {
                        "appId": "123456",
                        "status": "FAILED",
                        "lastUpdatedTime": "2025-02-04T15:32:06.693027Z",
                        "type": "RTC",
                        "trunkId": "",
                        "serviceId": ""
                    },
                    "lastUpdatedTime": None,
                    "type": "RTC",
                    "trunkId": "",
                    "serviceId": ""
                },
                "callbackUrl": ""
            }
        ],
        "nextPageToken": "CgtwaG9uZU51bWJlchJnCjl0eXBlLmdvb2dsZWFwaXMuY29tL3NpbmNoLn==",
        "totalSize": 10
    }


def assert_voice_configuration(voice_config):
    assert voice_config.app_id == ""
    assert voice_config.scheduled_voice_provisioning.app_id == "123456"
    assert voice_config.scheduled_voice_provisioning.status == "FAILED"
    expected_last_updated_time = (
        datetime(2025, 2, 4, 15, 32, 6, 693027, tzinfo=timezone.utc))
    assert voice_config.scheduled_voice_provisioning.last_updated_time == expected_last_updated_time
    assert voice_config.scheduled_voice_provisioning.type == "RTC"
    assert voice_config.scheduled_voice_provisioning.trunk_id == ""
    assert voice_config.scheduled_voice_provisioning.service_id == ""


def assert_sms_configuration(sms_config):
    assert sms_config.service_plan_id == "al_2308"
    assert sms_config.scheduled_provisioning is None
    assert sms_config.campaign_id == ""


def test_list_active_numbers_response_expects_correct_mapping(test_data):
    """
    Check if response is handled and mapped to the appropriate fields correctly.
    """
    response = ListActiveNumbersResponse(**test_data)
    assert hasattr(response, "content")
    assert response.content == response.active_numbers

    number = response.active_numbers[0]
    assert number.phone_number == "+12085088605"
    assert number.project_id == "37b62a7b-0177-429a-bb0b-e10f848de0b8"
    assert number.display_name == ""
    assert number.region_code == "US"
    assert number.type == "LOCAL"
    assert number.capability == ["SMS", "VOICE"]
    assert number.money.currency_code == "EUR"
    assert number.money.amount == Decimal("0.80")
    assert number.payment_interval_months == 1
    expected_next_charge_date = datetime(
        2025, 3, 4, 15, 28, 16, 449951, tzinfo=timezone.utc
    )
    assert number.next_charge_date == expected_next_charge_date
    assert number.expire_at is None
    assert_sms_configuration(number.sms_configuration)
    assert_voice_configuration(number.voice_configuration)
    assert response.next_page_token == "CgtwaG9uZU51bWJlchJnCjl0eXBlLmdvb2dsZWFwaXMuY29tL3NpbmNoLn=="
    assert response.total_size == 10
