import os

from sinch import SinchClient

MOCKSERVER_BASE_URL = os.getenv('MOCKSERVER_BASE_URL', 'https://sinch-sdk-mockserver.sliplane.app')

AUTHENTICATION_ORIGIN = f'{MOCKSERVER_BASE_URL}/authentication'
NUMBERS_ORIGIN = f'{MOCKSERVER_BASE_URL}/numbers'
SMS_ORIGIN = f'{MOCKSERVER_BASE_URL}/sms'
NUMBER_LOOKUP_ORIGIN = f'{MOCKSERVER_BASE_URL}/number-lookup'
CONVERSATION_ORIGIN = f'{MOCKSERVER_BASE_URL}/conversation'


def create_test_client():
    """Creates a Sinch client with test configuration for all domains"""
    client_params = {
        'project_id': 'tinyfrog-jump-high-over-lilypadbasin',
        'key_id': 'keyId',
        'key_secret': 'keySecret',
    }
    client = SinchClient(**client_params)
    client.configuration.auth_origin = AUTHENTICATION_ORIGIN
    client.configuration.numbers_origin = NUMBERS_ORIGIN
    client.configuration.sms_origin = SMS_ORIGIN
    client.configuration.number_lookup_origin = NUMBER_LOOKUP_ORIGIN
    client.configuration.conversation_origin = CONVERSATION_ORIGIN
    return client


def create_test_client_with_service_plan_id():
    """Creates a Sinch client configured for servicePlanId authentication (SMS legacy auth)"""
    client = SinchClient(
        service_plan_id='CappyPremiumPlan',
        sms_api_token='HappyCappyToken',
    )
    client.configuration.auth_origin = AUTHENTICATION_ORIGIN
    client.configuration.sms_origin = SMS_ORIGIN
    client.configuration.sms_origin_with_service_plan_id = SMS_ORIGIN
    return client
