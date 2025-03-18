from datetime import datetime, timezone
from sinch.domains.numbers.models.v1 import ActiveNumber
from sinch.domains.numbers.models.v1.errors import NotFoundError
from sinch.domains.numbers.models.v1.shared import (
    ScheduledSmsProvisioning, SmsConfigurationResponse, VoiceConfigurationResponse
)

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
    config = SmsConfigurationResponse.model_validate(data)

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
        "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
        "scheduledVoiceProvisioning": {
            "type": "RTC",
            "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
            "status": "ACTIVE",
            "appId": "test_app"
        }
    }
    config = VoiceConfigurationResponse.model_validate(data)

    assert config.type == "RTC"
    assert config.app_id == "test_app"
    assert (config.last_updated_time ==
            datetime(2025, 1, 24, 9, 32, 27, 437000,
                     tzinfo=timezone.utc))
    assert config.scheduled_voice_provisioning is not None
    assert config.scheduled_voice_provisioning.type == "RTC"
    assert config.scheduled_voice_provisioning.status == "ACTIVE"

def test_voice_configuration_fax_valid_expects_parsed_data():
    """
    Test a valid FAX voice configuration
    """
    data = {
        "type": "FAX",
        "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
        "scheduledVoiceProvisioning": {
            "type": "FAX",
            "lastUpdatedTime": "2025-01-24T09:32:27.437Z",
            "status": "ACTIVE",
            "serviceId": "test_service"
        }
    }
    config = VoiceConfigurationResponse.model_validate(data)

    assert config.type == "FAX"
    assert config.scheduled_voice_provisioning is not None
    assert config.scheduled_voice_provisioning.type == "FAX"
    assert config.scheduled_voice_provisioning.status == "ACTIVE"
    assert config.scheduled_voice_provisioning.service_id == "test_service"

def test_not_found_error_deserialize_with_snake_case():
    data = {
        'code': 404,
        'message': '',
        'status': 'NOT_FOUND',
        'details': [
            {
                'type': 'ResourceInfo',
                'resourceType': 'AvailableNumber',
                'resourceName': '+1234567890',
                'owner': '',
                'description': ''
            }
        ]
    }

    not_found_error = NotFoundError.model_validate(data)

    assert not_found_error.code == 404
    assert not_found_error.message == ''
    assert not_found_error.status == 'NOT_FOUND'
    assert not_found_error.details[0].type == 'ResourceInfo'
    assert not_found_error.details[0].resource_type == 'AvailableNumber'
    assert not_found_error.details[0].resource_name == '+1234567890'
    assert not_found_error.details[0].owner == ''
    assert not_found_error.details[0].description == ''

def test_activate_number_response_expects_all_fields_mapped_correctly():
    """
    Expects all fields to map correctly from camelCase input,
    converts nested keys to snake_case, and handles dynamic fields
    """
    data = {
        "phoneNumber": "+12025550134",
        "displayName": "string",
        "regionCode": "US",
        "type": "MOBILE",
        "capability": ["SMS"],
        "money": {"currencyCode": "USD", "amount": "2.00"},
        "paymentIntervalMonths": 0,
        "nextChargeDate": "2025-01-22T13:19:31.095Z",
        "expireAt": "2025-03-29T13:19:31.095Z",
        "callbackUrl": "https://www.your-callback-server.com/callback",
    }
    response = ActiveNumber(**data)

    assert response.phone_number == "+12025550134"
    assert response.display_name == "string"
    assert response.region_code == "US"
    assert response.type == "MOBILE"
    assert response.capability == ["SMS"]
    assert response.money.currency_code == "USD"
    assert response.payment_interval_months == 0
    expected_next_charge_data = (
        datetime(2025, 1, 22, 13, 19, 31, 95000, tzinfo=timezone.utc))
    assert response.next_charge_date == expected_next_charge_data
    expected_expire_at = (
        datetime(2025, 3, 29, 13, 19, 31, 95000, tzinfo=timezone.utc))
    assert response.expire_at == expected_expire_at
    assert response.callback_url == "https://www.your-callback-server.com/callback"
