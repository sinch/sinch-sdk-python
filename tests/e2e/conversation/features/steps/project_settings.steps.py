from behave import given, when, then
from sinch.domains.conversation.api.v1.project_settings_apis import ProjectSettings


PROJECT_ID = '123coffee-dada-beef-cafe-baadc0de5678'


@given('the Conversation service "ProjectSettings" is available')
def step_project_settings_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.project_settings, ProjectSettings), 'ProjectSettings service is not available'
    context.project_settings = context.sinch.conversation.project_settings


def _validate_project_settings(response, unified_contact_id_enabled):
    assert response is not None, 'Project settings response should not be None'
    assert response.project_id == PROJECT_ID, f'Expected project_id "{PROJECT_ID}", got "{response.project_id}"'
    enabled = response.settings.contact_settings.unified_contact_id_enabled
    assert enabled is unified_contact_id_enabled, f'Expected unified_contact_id_enabled {unified_contact_id_enabled}, got {enabled}'


@when('I send a request to create project settings')
def step_create_project_settings(context):
    context.create_response = context.project_settings.create(
        contact_settings={'unified_contact_id_enabled': False}
    )


@then('the project settings are created')
def step_validate_create_project_settings(context):
    _validate_project_settings(context.create_response, False)


@when('I send a request to retrieve project settings')
def step_get_project_settings(context):
    context.get_response = context.project_settings.get()


@then('the response contains the project settings details')
def step_validate_get_project_settings(context):
    _validate_project_settings(context.get_response, False)


@when('I send a request to update project settings')
def step_update_project_settings(context):
    context.update_response = context.project_settings.update(
        contact_settings={'unified_contact_id_enabled': True}
    )


@then('the response contains the project settings details with updated properties')
def step_validate_update_project_settings(context):
    _validate_project_settings(context.update_response, True)


@when('I send a request to delete project settings')
def step_delete_project_settings(context):
    context.delete_response = context.project_settings.delete()


@then('the delete project settings response contains no data')
def step_validate_delete_project_settings(context):
    assert context.delete_response is None, 'Delete project settings should not return data'
