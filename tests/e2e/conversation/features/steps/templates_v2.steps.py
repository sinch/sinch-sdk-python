from datetime import datetime, timezone

from behave import given, when, then
from sinch.domains.conversation.templates.api.v2.templates_apis import (
    Templates,
)
from sinch.domains.conversation.templates.models.v2.shared.template_translation import (
    TemplateTranslationListMessage,
    TemplateTranslationTextMessage,
)


@given('the Conversation service "TemplatesV2" is available')
def step_templates_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.templates, Templates), 'Templates service is not available'
    context.templates = context.sinch.conversation.templates


@when('I send a request to create a conversation template with the V2 API')
def step_create_template(context):
    context.template = context.templates.create(
        id='01HVN010MG3B9N6X323JAFN59P',
        default_translation='en-US',
        description='Text template V2',
        translations=[
            {
                'language_code': 'en-US',
                'version': '3',
                'text_message': {
                    'text': 'Hello ${name}. Text message template created with V2 API',
                },
                'variables': [
                    {'key': 'name', 'preview_value': 'Professor Jones'},
                ],
            },
        ],
    )


@then('the conversation template V2 is created')
def step_validate_created_template(context):
    template = context.template
    assert template.id == '01HVN010MG3B9N6X323JAFN59P', f'Expected template.id to be "01HVN010MG3B9N6X323JAFN59P", got "{template.id}"'
    assert template.version == 1, f'Expected template.version to be 1, got {template.version}'
    assert len(template.translations) == 1, f'Expected 1 translation, got {len(template.translations)}'
    assert template.translations[0].version == '3', f'Expected translation version to be "3", got "{template.translations[0].version}"'


@when('I send a request to list the conversation templates with the V2 API')
def step_list_templates(context):
    context.templates_list = context.templates.list().content()


@then('the response contains the list of conversation templates with the V2 structure')
def step_validate_templates_list(context):
    assert len(context.templates_list) == 2, f'Expected 2 templates, got {len(context.templates_list)}'


@then('for each templateV2 in the templateV2 list response, it defines a translation with version "latest" on top of each current translation version')
def step_validate_latest_translations(context):
    for template in context.templates_list:
        assert template.version is not None, 'Expected template.version to be set'
        latest_count = sum(1 for t in template.translations if t.version == 'latest')
        other_count = len(template.translations) - latest_count
        assert latest_count == other_count, f'Expected as many "latest" translations as versioned ones, got {latest_count} and {other_count}'


@when('I send a request to list the translations for a template with the V2 API')
def step_list_translations(context):
    context.translations_list = context.templates.list_translations(
        template_id='01W4FFL35P4NC4K35TEMPLATEV2',
    ).content()


@then('the response contains the list of translations for a template with the V2 structure')
def step_validate_translations_list(context):
    translations = context.translations_list
    assert len(translations) == 2, f'Expected 2 translations, got {len(translations)}'
    assert all(t.version != 'latest' for t in translations), 'Expected no "latest" translation'


@when('I send a request to retrieve a conversation template with the V2 API')
def step_get_template(context):
    context.template = context.templates.get(
        template_id='01HVN010MG3B9N6X323JAFN59P',
    )


@then('the response contains the conversation template details with the V2 structure')
def step_validate_template_details(context):
    template = context.template
    expected_time = datetime(2024, 6, 6, 14, 42, 42, tzinfo=timezone.utc)
    assert template.id == '01HVN010MG3B9N6X323JAFN59P', f'Expected template.id to be "01HVN010MG3B9N6X323JAFN59P", got "{template.id}"'
    assert template.description == 'Text template V2', f'Expected description to be "Text template V2", got "{template.description}"'
    assert template.version == 1, f'Expected template.version to be 1, got {template.version}'
    assert len(template.translations) == 2, f'Expected 2 translations, got {len(template.translations)}'
    translation = next(t for t in template.translations if t.version != 'latest')
    assert isinstance(translation, TemplateTranslationTextMessage), f'Expected a text translation, got {type(translation).__name__}'
    assert translation.language_code == 'en-US', f'Expected language_code to be "en-US", got "{translation.language_code}"'
    assert translation.version == '3', f'Expected translation version to be "3", got "{translation.version}"'
    assert translation.create_time == expected_time, f'Unexpected translation create_time {translation.create_time}'
    assert translation.update_time == expected_time, f'Unexpected translation update_time {translation.update_time}'
    assert len(translation.variables) == 1, f'Expected 1 variable, got {len(translation.variables)}'
    assert translation.text_message.text, 'Expected text_message.text to be set'
    assert translation.channel_template_overrides == {}, f'Expected no channel template overrides, got {translation.channel_template_overrides}'
    assert template.default_translation == 'en-US', f'Expected default_translation to be "en-US", got "{template.default_translation}"'
    assert template.create_time == expected_time, f'Unexpected template create_time {template.create_time}'
    assert template.update_time == expected_time, f'Unexpected template update_time {template.update_time}'


@when('I send a request to update a conversation template with the V2 API')
def step_update_template(context):
    context.current_version = 1
    context.template = context.templates.update(
        template_id='01HVN010MG3B9N6X323JAFN59P',
        version=context.current_version,
        description='Updated description v2',
        default_translation='en-US',
        translations=[
            {
                'language_code': 'en-US',
                'version': '1',
                'list_message': {
                    'title': 'Choose your icecream flavor',
                    'description': 'The best icecream in town!',
                    'sections': [
                        {
                            'title': 'Fruit flavors',
                            'items': [
                                {'choice': {'title': 'Strawberry', 'postback_data': 'Strawberry postback'}},
                                {'choice': {'title': 'Blueberry', 'postback_data': 'Blueberry postback'}},
                            ],
                        },
                        {
                            'title': 'Other flavors',
                            'items': [
                                {'choice': {'title': 'Chocolate', 'postback_data': 'Chocolate postback'}},
                                {'choice': {'title': 'Vanilla', 'postback_data': 'Vanilla postback'}},
                            ],
                        },
                    ],
                },
            },
        ],
    )


@then('the response contains the conversation template details with updated data with the V2 structure')
def step_validate_updated_template(context):
    template = context.template
    assert template.id == '01HVN010MG3B9N6X323JAFN59P', f'Expected template.id to be "01HVN010MG3B9N6X323JAFN59P", got "{template.id}"'
    assert template.description == 'Updated description v2', f'Expected description to be "Updated description v2", got "{template.description}"'
    assert template.version == context.current_version + 1, f'Expected template.version to be {context.current_version + 1}, got {template.version}'
    assert len(template.translations) == 1, f'Expected 1 translation, got {len(template.translations)}'
    assert template.default_translation == 'en-US', f'Expected default_translation to be "en-US", got "{template.default_translation}"'
    assert template.create_time == datetime(2024, 6, 6, 14, 42, 42, tzinfo=timezone.utc), f'Unexpected create_time {template.create_time}'
    assert template.update_time == datetime(2024, 6, 6, 15, 45, 45, tzinfo=timezone.utc), f'Unexpected update_time {template.update_time}'
    assert isinstance(template.translations[0], TemplateTranslationListMessage), f'Expected a list translation, got {type(template.translations[0]).__name__}'
    assert template.translations[0].list_message is not None, 'Expected list_message to be set'


@when('I send a request to delete a conversation template with the V2 API')
def step_delete_template(context):
    context.delete_response = context.templates.delete(
        template_id='01W4FFL35P4NC4K35TEMPLATEV2',
    )


@then('the delete conversation template response V2 contains no data')
def step_validate_deleted_template(context):
    assert context.delete_response is None, f'Expected no data, got {context.delete_response}'
