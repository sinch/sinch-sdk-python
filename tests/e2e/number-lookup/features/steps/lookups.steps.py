from datetime import datetime, timezone
from behave import given, when, then
from sinch.domains.number_lookup.models.v1.response import LookupNumberResponse


@given('the Number Lookup service is available')
def step_service_is_available(context):
    assert hasattr(context, 'sinch') and context.sinch, 'Sinch client was not initialized'


@when('I send a request to lookup for a phone number with no additional features')
def step_lookup_number_no_features(context):
    context.response = context.sinch.number_lookup.lookup(
        number='+12016666666'
    )


@then('the response contains the details of the phone number lookup with line details only')
def step_validate_lookup_line_only(context):
    data: LookupNumberResponse = context.response
    assert data.number == '+12016666666'
    assert data.country_code == 'US'
    assert data.trace_id == '84c1fd4063c38d9f3900d06e56542d48'
    assert data.line.carrier == 'T-Mobile USA'
    assert data.line.type == 'Mobile'
    assert data.line.mobile_country_code == '310'
    assert data.line.mobile_network_code == '260'
    assert data.line.ported is None
    assert data.line.porting_date is None
    assert data.line.error is None
    assert data.sim_swap is None
    assert data.voip_detection is None
    assert data.rnd is None


@when('I send a request to lookup for a phone number with all the features')
def step_lookup_number_all_features(context):
    context.response = context.sinch.number_lookup.lookup(
        number='+12015555555',
        features=['LineType', 'RND', 'SimSwap', 'VoIPDetection'],
        rnd_feature_options={'contactDate': '2025-09-09'}
    )


@then('the response contains the details of the phone number lookup with all the features')
def step_validate_lookup_all_features(context):
    data: LookupNumberResponse = context.response
    assert data.number == '+12015555555'
    assert data.country_code == 'US'
    assert data.trace_id == '5c817a6b7351d80a6b1d8007e5c145b8'
    
    assert data.line is not None
    assert data.line.carrier == 'AT&T'
    assert data.line.type == 'Mobile'
    assert data.line.mobile_country_code == '310'
    assert data.line.mobile_network_code == '070'
    assert data.line.ported is True
    assert data.line.porting_date == datetime(2010, 8, 7, 23, 45, 49, tzinfo=timezone.utc)
    assert data.line.error is None
    
    assert data.sim_swap.swapped is None
    assert data.sim_swap.swap_period is None
    assert data.sim_swap.error.status == 100
    assert data.sim_swap.error.title == 'Feature Disabled'
    assert data.sim_swap.error.detail == 'SimSwap feature is currently disabled.'
    
    assert data.voip_detection is not None
    assert data.voip_detection.probability is None
    assert data.voip_detection.error.status == 100
    assert data.voip_detection.error.title == 'Feature Disabled'
    assert data.voip_detection.error.detail == 'VoIPDetection feature is currently disabled.'
    
    assert data.rnd is not None
    assert data.rnd.disconnected is None
    assert data.rnd.error is not None
    assert data.rnd.error.status == 100
    assert data.rnd.error.title == 'Feature Disabled'
    assert data.rnd.error.detail == 'RND feature is currently disabled.'
