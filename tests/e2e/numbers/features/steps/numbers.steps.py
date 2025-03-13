import inspect
from datetime import timezone, datetime
from behave import given, when, then
from decimal import Decimal
from sinch.domains.numbers.exceptions import NumberNotFoundException
from sinch.domains.numbers.models.v1 import RentAnyNumberResponse
from sinch.domains.numbers.models.v1.errors import NotFoundError
from sinch.domains.numbers.models.v1.shared_params import ActiveNumber


def execute_sync_or_async(context,call):
    """
    Ensures proper execution of both synchronous and asynchronous calls.
    - If the call is synchronous, it executes directly.
    - If the call is a coroutine (async), it runs using asyncio
    This abstracts away execution differences, allowing test steps to be written uniformly.
    """
    if call is None:
        return None
    if inspect.iscoroutine(call):
        # Reuse the single loop created in before_all
        return context.loop.run_until_complete(call)
    else:
        return call

@given('the Numbers service is available')
def step_service_is_available(context):
    """Ensures the Sinch client is initialized"""
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'

@when('I send a request to search for available phone numbers')
def step_search_available_numbers(context):
    response = context.sinch.numbers.available.list(
        region_code='US',
        number_type='LOCAL'
    )
    context.response = execute_sync_or_async(context, response)

@then('the response contains "{count}" available phone numbers')
def step_check_available_numbers_count(context, count):
    data = context.response
    assert len(data) == int(count), f'Expected {count}, got {len(data)}'

@then('a phone number contains all the expected properties')
def step_check_number_properties(context):
    number = context.response[0]
    assert number.phone_number == '+12013504948'
    assert number.region_code == 'US'
    assert number.type == 'LOCAL'
    assert number.capability == ['SMS', 'VOICE']
    assert number.setup_price.currency_code == 'EUR'
    assert number.setup_price.amount == Decimal('0.80')
    assert number.monthly_price.currency_code == 'EUR'
    assert number.monthly_price.amount == Decimal('0.80')
    assert number.payment_interval_months == 1
    assert number.supporting_documentation_required == True

@when('I send a request to check the availability of the phone number "{phone_number}"')
def step_check_number_availability(context, phone_number):
    try:
        response = context.sinch.numbers.available.check_availability(phone_number)
        context.response = execute_sync_or_async(context, response)
    except NumberNotFoundException as e:
        context.error = e

@then('the response displays the phone number "{phone_number}" details')
def step_validate_number_details(context, phone_number):
    data = context.response
    assert data.phone_number == phone_number, f'Expected {phone_number}, got {data.phone_number}'

@then('the response contains an error about the number "{phone_number}" not being available')
def step_check_unavailable_number(context, phone_number):
    data: NotFoundError = context.error.args[0]
    assert data.code == 404
    assert data.status == 'NOT_FOUND'
    assert data.details[0].resource_name == phone_number

@when('I send a request to rent a number with some criteria')
def step_rent_any_number(context):
    response = context.sinch.numbers.available.rent_any(
        region_code = 'US',
        type_ = 'LOCAL',
        capabilities = ['SMS', 'VOICE'],
        sms_configuration = {
            'service_plan_id': 'SpaceMonkeySquadron',
        },
        voice_configuration = {
            'type': 'RTC',
            'app_id': 'sunshine-rain-drop-very-beautifulday'
        },
        number_pattern = {
            'pattern': '7654321',
            'search_pattern': 'END'
        },
    )
    context.response = execute_sync_or_async(context, response)

@then('the response contains a rented phone number')
def step_validate_rented_number(context):
    data: RentAnyNumberResponse = context.response
    assert data.phone_number == '+12017654321'
    assert data.project_id == '123c0ffee-dada-beef-cafe-baadc0de5678'
    assert data.display_name == ''
    assert data.region_code == 'US'
    assert data.type == 'LOCAL'
    assert data.capability == ['SMS', 'VOICE']
    assert data.money.currency_code == 'EUR'
    assert data.money.amount == Decimal('0.80')
    assert data.payment_interval_months == 1
    assert data.next_charge_date == datetime.fromisoformat(
        '2024-06-06T14:42:42.022227+00:00'
    ).astimezone(tz=timezone.utc)
    assert data.expire_at == None
    assert data.callback_url == ''
    assert data.sms_configuration.service_plan_id == ''
    assert data.sms_configuration.campaign_id == ''
    assert data.sms_configuration.scheduled_provisioning.service_plan_id == 'SpaceMonkeySquadron'
    assert data.sms_configuration.scheduled_provisioning.campaign_id == ''
    assert data.sms_configuration.scheduled_provisioning.status == 'WAITING'
    assert data.sms_configuration.scheduled_provisioning.last_updated_time == datetime.fromisoformat(
        '2024-06-06T14:42:42.596223+00:00'
    ).astimezone(tz=timezone.utc)
    assert data.sms_configuration.scheduled_provisioning.error_codes == []
    assert data.voice_configuration.type == 'RTC'
    assert data.voice_configuration.app_id == ''
    assert data.voice_configuration.trunk_id == ''
    assert data.voice_configuration.service_id == ''
    assert data.voice_configuration.scheduled_voice_provisioning.type == 'RTC'
    assert data.voice_configuration.scheduled_voice_provisioning.app_id == 'sunshine-rain-drop-very-beautifulday'
    assert data.voice_configuration.scheduled_voice_provisioning.trunk_id == ''
    assert data.voice_configuration.scheduled_voice_provisioning.service_id == ''
    assert data.voice_configuration.scheduled_voice_provisioning.status == 'WAITING'
    assert data.voice_configuration.scheduled_voice_provisioning.last_updated_time == datetime.fromisoformat(
        '2024-06-06T14:42:42.604092+00:00'
    ).astimezone(tz=timezone.utc)

@when('I send a request to rent the phone number "{phone_number}"')
def step_rent_specific_number(context, phone_number):
    response = context.sinch.numbers.available.activate(
        phone_number = phone_number,
        sms_configuration= {
            'service_plan_id': 'SpaceMonkeySquadron',
        },
        voice_configuration= {
            'app_id': 'sunshine-rain-drop-very-beautifulday'
        }
    )
    context.response = execute_sync_or_async(context, response)

@then('the response contains this rented phone number "{phone_number}"')
def step_validate_rented_specific_number(context, phone_number):
    data: ActiveNumber = context.response
    assert data.phone_number == phone_number, f'Expected {phone_number}, got {data.phone_number}'

@when('I send a request to rent the unavailable phone number "{phone_number}"')
def step_rent_unavailable_number(context, phone_number):
    try:
        response = context.sinch.numbers.available.activate(
            phone_number=phone_number,
            sms_configuration={
                'service_plan_id': 'SpaceMonkeySquadron',
            },
            voice_configuration={
                'app_id': 'sunshine-rain-drop-very-beautifulday'
            }
        )
        context.response = execute_sync_or_async(context, response)
    except NumberNotFoundException as e:
        context.error = e

@when("I send a request to list the phone numbers")
def step_when_list_phone_numbers(context):
    response = context.sinch.numbers.active.list(
        region_code='US',
        number_type='LOCAL'
    )
    # Get the first page
    response = execute_sync_or_async(context, response)
    context.response = response.content()


@then('the response contains "{count}" phone numbers')
def step_then_response_contains_x_phone_numbers(context, count):
    assert len(context.response) == int(count), \
        f'Expected {count}, got {len(context.response)}'

@when("I send a request to list all the phone numbers")
def step_when_list_all_phone_numbers(context):
    response = context.sinch.numbers.active.list(
        region_code='US',
        number_type='LOCAL'
    )
    active_numbers_list = []

    response = execute_sync_or_async(context, response)
    if inspect.isasyncgen(response.iterator()):
        async def collect_async_numbers():
            async for number in response.iterator():
                active_numbers_list.append(number)

        execute_sync_or_async(context, collect_async_numbers())
    else:
        for number in response.iterator():
            active_numbers_list.append(number)

    context.active_numbers_list = active_numbers_list

@then('the phone numbers list contains "{count}" phone numbers')
def step_then_phone_numbers_list_contains_x_phone_numbers(context, count):
    assert len(context.active_numbers_list) == int(count), f'Expected {count}, got {len(context.active_numbers_list)}'
    phone_number1 = context.active_numbers_list[0]
    assert phone_number1.voice_configuration.type == 'FAX'
    assert phone_number1.voice_configuration.service_id == '01W4FFL35P4NC4K35FAXSERVICE'
    phone_number2 = context.active_numbers_list[1]
    assert phone_number2.voice_configuration.type == 'EST'
    assert phone_number2.voice_configuration.trunk_id == '01W4FFL35P4NC4K35SIPTRUNK00'
    phone_number3 = context.active_numbers_list[2]
    assert phone_number3.voice_configuration.type == 'RTC'
    assert phone_number3.voice_configuration.app_id == 'sunshine-rain-drop-very-beautifulday'

@when('I send a request to update the phone number "{phone_number}"')
def step_when_update_phone_number(context, phone_number):
    pass  # Placeholder

@then('the response contains a phone number with updated parameters')
def step_then_response_contains_updated_number(context):
    pass  # Placeholder

@when('I send a request to retrieve the phone number "{phone_number}"')
def step_when_retrieve_phone_number(context, phone_number):
    pass  # Placeholder

@then('the response contains details about the phone number "{phone_number}"')
def step_then_response_contains_phone_details(context, phone_number):
    pass  # Placeholder

@then('the response contains details about the phone number "{phone_number}" with an SMS provisioning error')
def step_then_response_contains_sms_provisioning_error(context, phone_number):
    pass  # Placeholder

@then('the response contains an error about the number "{phone_number}" not being a rented number')
def step_then_response_contains_error_not_rented(context, phone_number):
    pass  # Placeholder

@when('I send a request to release the phone number "{phone_number}"')
def step_when_release_phone_number(context, phone_number):
    pass  # Placeholder

@then('the response contains details about the phone number "{phone_number}" to be released')
def step_then_response_contains_released_number(context, phone_number):
    pass  # Placeholder
