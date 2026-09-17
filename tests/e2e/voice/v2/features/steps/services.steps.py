from behave import given, when, then
from sinch.domains.voice.api.v2.services_apis import Services
from sinch.domains.voice.models.v2.services.response.service_response import (
    ServiceResponse,
)

SERVICE_ID = "3c4d5e6f-7a8b-4901-c234-d5e6f7a8b901"


@given('the Voice-V2 service "Services" is available')
def step_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.voice.v2.services, Services), 'Voice-V2 "Services" service is not available'
    context.services = context.sinch.voice.v2.services


@when('I send a request to create a Voice-V2 service')
def step_create_service(context):
    context.response = context.services.create(name='Example service')


@then('the response contains the information about the Voice-V2 service created')
def step_validate_create_service(context):
    data: ServiceResponse = context.response
    assert data.service_id == '1a2b3c4d-5e6f-4789-a012-b3c4d5e6f789'
    assert data.project_id == 'c3d4e5f6-a7b8-4901-c234-d5e6f7a8b901'
    assert data.name == 'Example service'
    assert data.is_default is False


@when('I send a request to list Voice-V2 services')
def step_list_services(context):
    context.response = context.services.list(page_size=2)


@then('the response contains "{count}" Voice-V2 services')
def step_validate_services_count(context, count):
    expected_count = int(count)
    assert len(context.response.content()) == expected_count, \
        f'Expected {expected_count}, got {len(context.response.content())}'


@when('I send a request to list all the Voice-V2 services')
def step_list_all_services(context):
    response = context.services.list(page_size=2)
    context.services_list = list(response.iterator())


@then('the services list contains "{count}" Voice-V2 services')
def step_validate_services_list_count(context, count):
    expected_count = int(count)
    assert len(context.services_list) == expected_count, \
        f'Expected {expected_count}, got {len(context.services_list)}'


@when('I iterate manually over the Voice-V2 services pages')
def step_iterate_manually_services(context):
    context.list_response = context.services.list(page_size=2)

    context.services_list = []
    context.pages_iteration = 0
    reached_end_of_pages = False

    while not reached_end_of_pages:
        context.services_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_end_of_pages = True


@then('the services iteration result contains the data from "{count}" Voice-V2 service pages')
def step_validate_services_pages_count(context, count):
    expected_pages_count = int(count)
    assert context.pages_iteration == expected_pages_count, \
        f'Expected {expected_pages_count}, got {context.pages_iteration}'


@when('I send a request to get Voice-V2 service details')
def step_get_service_details(context):
    context.response = context.services.get(service_id=SERVICE_ID)


@then('the response contains the Voice-V2 service details')
def step_validate_get_service_details(context):
    data: ServiceResponse = context.response
    assert data.service_id == SERVICE_ID
    assert data.project_id == 'c3d4e5f6-a7b8-4901-c234-d5e6f7a8b901'
    assert data.name == 'Example service 2'
    assert data.is_default is False
    assert data.call_behavior.type == 'NONE'


@when('I send a request to update a Voice-V2 service')
def step_update_service(context):
    context.response = context.services.update(
        service_id=SERVICE_ID,
        description='Service with webhooks',
        call_behavior={
            'type': 'EVENT_DESTINATION',
            'event_destination': {
                'url': 'https://example.com/webhook',
                'fallback_url': 'https://example.com/fallback',
            },
        },
    )


@then('the response contains the information about the Voice-V2 service updated')
def step_validate_update_service(context):
    data: ServiceResponse = context.response
    assert data.service_id == SERVICE_ID
    assert data.description == 'Service with webhooks'
    assert data.call_behavior.type == 'EVENT_DESTINATION'
    assert data.call_behavior.event_destination.url == 'https://example.com/webhook'
    assert (
        data.call_behavior.event_destination.fallback_url
        == 'https://example.com/fallback'
    )


@when('I send a request to delete a Voice-V2 service')
def step_delete_service(context):
    context.response = context.services.delete(service_id=SERVICE_ID)


@then('the response confirms the Voice-V2 service was deleted')
def step_validate_delete_service(context):
    assert context.response is None
