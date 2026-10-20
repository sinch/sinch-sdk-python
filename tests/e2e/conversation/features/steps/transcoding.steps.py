import json

from behave import given, when, then
from sinch.domains.conversation.api.v1.transcoding_apis import Transcoding


@given('the Conversation service "Transcoding" is available')
def step_transcoding_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.transcoding, Transcoding), 'Transcoding service is not available'
    context.transcoding = context.sinch.conversation.transcoding


@when('I send a request to transcode a location message')
def step_transcode_location_message(context):
    context.transcode_channels = [
        'APPLEBC', 'INSTAGRAM', 'KAKAOTALK', 'KAKAOTALKCHAT', 'LINE', 'MESSENGER',
        'RCS', 'SMS', 'TELEGRAM', 'VIBER', 'WECHAT', 'WHATSAPP',
    ]
    context.transcode_message_response = context.transcoding.transcode_message(
        app_id='01W4FFL35P4NC4K35CONVAPP001',
        app_message={
            'location_message': {
                'title': "Phare d'Eckmühl",
                'label': 'Pointe de Penmarch',
                'coordinates': {'latitude': 47.7981899, 'longitude': -4.3727685},
            }
        },
        channels=context.transcode_channels,
    )


@then('the location message is transcoded for all the channels')
def step_validate_transcoded_location_message(context):
    transcoded = context.transcode_message_response.transcoded_message
    assert transcoded is not None, 'Transcoded message should not be None'
    for channel in context.transcode_channels:
        assert transcoded.get(channel), f'Expected a transcoded message for channel {channel}'
    expected_whatsapp = {
        'to': '{{to}}',
        'type': 'location',
        'recipient_type': 'individual',
        'location': {
            'name': "Phare d'Eckmühl",
            'address': 'Pointe de Penmarch',
            'longitude': '-4.3727684',
            'latitude': '47.79819',
        },
        'messaging_product': 'whatsapp',
        'biz_opaque_callback_data': None,
    }
    assert json.loads(transcoded['WHATSAPP']) == expected_whatsapp, f'Unexpected WhatsApp message: {transcoded["WHATSAPP"]}'
