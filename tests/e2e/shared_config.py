from sinch import SinchClient


def create_test_client():
    """Creates a Sinch client with test configuration for all domains"""
    client_params = {
        'project_id': 'tinyfrog-jump-high-over-lilypadbasin',
        'key_id': 'keyId',
        'key_secret': 'keySecret',
    }
    client = SinchClient(**client_params)
    client.configuration.auth_origin = 'http://localhost:3011'
    client.configuration.numbers_origin = 'http://localhost:3013'
    client.configuration.sms_origin = 'http://localhost:3017'
    client.configuration.number_lookup_origin = 'http://localhost:3022'
    return client
