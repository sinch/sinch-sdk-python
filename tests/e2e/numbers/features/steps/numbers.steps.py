from datetime import timezone, datetime
from behave import given, when, then
from decimal import Decimal
from sinch import SinchClient
from sinch.domains.numbers.exceptions import NumberNotFoundException
from sinch.domains.numbers.models.available.activate_number_response import ActivateNumberResponse
from sinch.domains.numbers.models.available.rent_any_number_response import RentAnyNumberResponse
from sinch.domains.numbers.models.numbers import NotFoundError


@given('the Numbers service is available')
def step_service_is_available(context):
    sinch = SinchClient(
        project_id='tinyfrog-jump-high-over-lilypadbasin',
        key_id='keyId',
        key_secret='keySecret',
    )
    sinch.configuration.auth_origin = 'http://localhost:3011'
    sinch.configuration.numbers_origin = 'http://localhost:3013'
    context.sinch = sinch

@when('I send a request to search for available phone numbers')
def step_search_available_numbers(context):
    response = context.sinch.numbers.available.list(
        region_code='US',
        number_type='LOCAL'
    )
    context.response = response

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
        context.response = response
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
    sinch_client: SinchClient = context.sinch
    response = sinch_client.numbers.available.rent_any(
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
    context.response = response

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
    assert data.next_charge_date == datetime.fromisoformat('2024-06-06T14:42:42.022227Z').astimezone(tz=timezone.utc)
    assert data.expire_at == None
    assert data.callback_url == ''
    assert data.sms_configuration.service_plan_id == ''
    assert data.sms_configuration.campaign_id == ''
    assert data.sms_configuration.scheduled_provisioning.service_plan_id == 'SpaceMonkeySquadron'
    assert data.sms_configuration.scheduled_provisioning.campaign_id == ''
    assert data.sms_configuration.scheduled_provisioning.status == 'WAITING'
    assert data.sms_configuration.scheduled_provisioning.last_updated_time == datetime.fromisoformat('2024-06-06T14:42:42.596223Z').astimezone(tz=timezone.utc)
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
    assert data.voice_configuration.scheduled_voice_provisioning.last_updated_time == datetime.fromisoformat('2024-06-06T14:42:42.604092Z').astimezone(tz=timezone.utc)

@when('I send a request to rent the phone number "{phone_number}"')
def step_rent_specific_number(context, phone_number):
    sinch_client: SinchClient = context.sinch
    response = sinch_client.numbers.available.activate(
        phone_number = phone_number,
        sms_configuration= {
            'service_plan_id': 'SpaceMonkeySquadron',
        },
        voice_configuration= {
            'app_id': 'sunshine-rain-drop-very-beautifulday'
        }
    )
    context.response = response

@then('the response contains this rented phone number "{phone_number}"')
def step_validate_rented_specific_number(context, phone_number):
    data: ActivateNumberResponse = context.response
    assert data.phone_number == phone_number, f'Expected {phone_number}, got {data.phone_number}'

@when('I send a request to rent the unavailable phone number "{phone_number}"')
def step_rent_unavailable_number(context, phone_number):
    sinch_client: SinchClient = context.sinch
    try:
        response = sinch_client.numbers.available.activate(
            phone_number=phone_number,
            sms_configuration={
                'service_plan_id': 'SpaceMonkeySquadron',
            },
            voice_configuration={
                'app_id': 'sunshine-rain-drop-very-beautifulday'
            }
        )
        context.response = response
    except NumberNotFoundException as e:
        context.error = e

@when("I send a request to list the phone numbers")
def step_when_list_phone_numbers(context):
    pass  # Placeholder

@when("I send a request to list all the phone numbers")
def step_when_list_all_phone_numbers(context):
    pass  # Placeholder

@then('the response contains "{count}" phone numbers')
def step_then_response_contains_x_phone_numbers(context, count):
    pass  # Placeholder

@then('the phone numbers list contains "{count}" phone numbers')
def step_then_phone_numbers_list_contains_x_phone_numbers(context, count):
    pass  # Placeholder

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