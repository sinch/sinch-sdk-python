from sinch.domains.numbers.models.v1.internal.base import BaseModelConfigurationRequest


def test_to_camel_case_expects_parsed_standard_cases():
    """
    Test standard snake_case to camelCase conversion.
    """
    assert BaseModelConfigurationRequest._to_camel_case("foo_bar") == "fooBar"
    assert BaseModelConfigurationRequest._to_camel_case("hello_world") == "helloWorld"
    assert BaseModelConfigurationRequest._to_camel_case("this_is_a_test") == "thisIsATest"
    assert BaseModelConfigurationRequest._to_camel_case("PHONE_NUMBER") == "phoneNumber"
    assert BaseModelConfigurationRequest._to_camel_case("appId") == "appId"


def test_to_camel_case_expects_parsed_edge_cases():
    """
    Test edge cases like leading/trailing underscores and multiple underscores.
    """
    assert BaseModelConfigurationRequest._to_camel_case("foo__bar") == "foo_Bar"
    assert BaseModelConfigurationRequest._to_camel_case("foo___bar") == "foo__Bar"
    assert BaseModelConfigurationRequest._to_camel_case("trailing_") == "trailing_"


def test_to_camel_case_expects_empty_string():
    """
    Test empty string case.
    """
    assert BaseModelConfigurationRequest._to_camel_case("") == ""


def test_to_camel_case_expects_single_word():
    """
    Test single-word cases.
    """
    assert BaseModelConfigurationRequest._to_camel_case("word") == "word"
    assert BaseModelConfigurationRequest._to_camel_case("single") == "single"


def test_dict_expects_camel_case_input():
    """
    Test that the model correctly handles camelCase input.
    """
    data = {
        "sms_configuration": {"service_plan_id": "YOUR_SMS_servicePlanId"},
        "voice_configuration": {
            "appId": "YOUR_voice_appID",
            "type": "RTC"
        }
    }
    request = BaseModelConfigurationRequest(**data)
    response = request.model_dump()

    assert response == {
        'smsConfiguration': {'servicePlanId': 'YOUR_SMS_servicePlanId'},
        'voiceConfiguration': {'appId': 'YOUR_voice_appID', 'type': 'RTC'}
    }
