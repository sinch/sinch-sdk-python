from sinch import SinchClient


def before_all(context):
    """Initializes the Sinch client"""
    client_params = {
        'project_id': 'tinyfrog-jump-high-over-lilypadbasin',
        'key_id': 'keyId',
        'key_secret': 'keySecret',
    }
    context.sinch = SinchClient(**client_params)
    context.sinch.configuration.auth_origin = 'http://localhost:3011'
    context.sinch.configuration.numbers_origin = 'http://localhost:3013'
