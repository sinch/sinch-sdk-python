from datetime import datetime, timezone
from behave import given, when, then
from sinch.domains.conversation.api.v1.consents_apis import Consents


APP_ID = '01W4FFL35P4NC4K35CONVAPP001'
IDENTITY = '33612345678'


@given('the Conversation service "Consents" is available')
def step_consents_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'
    assert isinstance(context.sinch.conversation.consents, Consents), 'Consents service is not available'
    context.consents = context.sinch.conversation.consents


@when('I send a request to list the existing Consent Identities')
def step_list_consent_identities(context):
    context.list_response = context.consents.list_identities(
        app_id=APP_ID, list_type='OPT_OUT_ALL', page_size=10
    )
    context.identities_page = context.list_response.content()


@then('the response contains "{count}" Consent Identities')
def step_validate_list_consent_identities(context, count):
    assert len(context.identities_page) == int(count), f'Expected {count} identities, got {len(context.identities_page)}'


@when('I send a request to list all the Consent Identities')
def step_list_all_consent_identities(context):
    response = context.consents.list_identities(
        app_id=APP_ID, list_type='OPT_OUT_ALL', page_size=10
    )
    context.identities_list = list(response.iterator())


@when('I iterate manually over the Consent Identities pages')
def step_iterate_consent_identities_pages(context):
    context.list_response = context.consents.list_identities(
        app_id=APP_ID, list_type='OPT_OUT_ALL', page_size=10
    )
    context.identities_list = []
    context.pages_iteration = 0
    reached_end_of_pages = False

    while not reached_end_of_pages:
        context.identities_list.extend(context.list_response.content())
        context.pages_iteration += 1
        if context.list_response.has_next_page:
            context.list_response = context.list_response.next_page()
        else:
            reached_end_of_pages = True


@then('the Consent Identities list contains "{count}" Consent Identities')
def step_validate_consent_identities_list_count(context, count):
    assert len(context.identities_list) == int(count), f'Expected {count} identities, got {len(context.identities_list)}'


@then('the Consent Identities iteration result contains the data from "{count}" pages')
def step_validate_consent_identities_page_iteration_count(context, count):
    assert context.pages_iteration == int(count), f'Expected {count} pages, got {context.pages_iteration}'


@when('I send a request to list the Audit Records associated with an identity')
def step_list_audit_records(context):
    context.audit_records_response = context.consents.list_audit_records(
        app_id=APP_ID, identity=IDENTITY
    )


@then('the response contains list of the Audit Records associated with an identity')
def step_validate_audit_records(context):
    response = context.audit_records_response
    assert response.identity.identity == IDENTITY, f'Expected identity "{IDENTITY}", got "{response.identity.identity}"'
    assert len(response.audit_records) == 1, f'Expected 1 audit record, got {len(response.audit_records)}'
    record = response.audit_records[0]
    assert record.origin == 'ORIGIN_MO', f'Unexpected origin: {record.origin}'
    assert record.operation == 'OPERATION_INSERT', f'Unexpected operation: {record.operation}'
    assert record.list_type == 'OPT_OUT_ALL', f'Unexpected list_type: {record.list_type}'
    assert record.project_id == '123coffee-dada-beef-cafe-baadc0de5678', f'Unexpected project_id: {record.project_id}'
    assert record.app_id == APP_ID, f'Unexpected app_id: {record.app_id}'
    expected_datetime = datetime(2025, 6, 6, 14, 42, 56, 31323, tzinfo=timezone.utc)
    assert record.datetime == expected_datetime, f'Expected datetime {expected_datetime}, got {record.datetime}'
