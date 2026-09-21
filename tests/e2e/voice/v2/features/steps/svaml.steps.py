from behave import given, when, then
from sinch.domains.voice.api.v2.svaml_apis import Svaml
from sinch.domains.voice.models.v2.svaml.response.validate_svaml_response import (
    ValidateSvamlResponse,
)
from sinch.domains.voice.models.v2.svaml.response.describe_svaml_response import (
    DescribeSvamlResponse,
)

SVAML_PAYLOAD = {
    "commands": [
        {
            "command": "dial",
            "callName": "audio-notification",
            "from": {"type": "PHONE", "phone": {"number": "+12015555555"}},
            "to": {"type": "PHONE", "phone": {"number": "+12017777777"}},
            "dialTimeoutDurationSeconds": 30,
            "maxCallDurationSeconds": 300,
            "events": {
                "onAnswer": [
                    {
                        "command": "messages",
                        "messagesName": "notification",
                        "messages": [
                            {
                                "type": "PLAY",
                                "play": {
                                    "url": "https://samplelib.com/mp3/sample-12s.mp3"
                                },
                            },
                            {
                                "type": "SAY",
                                "say": {
                                    "text": "Hello! This is a test notification from Sinch. Your verification code is 4 8 3 7.",
                                    "voiceName": "Emma",
                                },
                            },
                        ],
                        "events": {"onFinish": [{"command": "hangup"}]},
                    }
                ]
            },
        }
    ]
}


@given('the Voice-V2 service "Svaml" is available')
def step_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.voice.v2.svaml, Svaml), 'Voice-V2 "Svaml" service is not available'
    context.svaml = context.sinch.voice.v2.svaml


@when('I send a request to validate a SVAML payload')
def step_validate_svaml(context):
    context.response = context.svaml.validate(commands=SVAML_PAYLOAD["commands"])


@then('the response confirms the SVAML payload is valid')
def step_validate_svaml_result(context):
    data: ValidateSvamlResponse = context.response
    assert data.is_valid is True


@when('I send a request to describe a SVAML payload')
def step_describe_svaml(context):
    context.response = context.svaml.describe(commands=SVAML_PAYLOAD["commands"])


@then('the response contains the description of the SVAML payload')
def step_describe_svaml_result(context):
    data: DescribeSvamlResponse = context.response
    assert data.description == (
        "1. A new call with name 'audio-notification' will be initiated to number +12017777777 with max duration set to 5 minutes.\n"
        " * on answer:\n"
        "     1. An audio file will be played from https://samplelib.com/mp3/sample-12s.mp3.\n"
        "     1. A TTS message will be played using the voice Emma.\n"
        "      * on finish:\n"
        "          1. The call will be disconnected"
    )
