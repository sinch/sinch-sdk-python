from tests.e2e.shared_config import create_test_client


def before_all(context):
    """Initializes the Sinch client"""
    context.sinch = create_test_client()
