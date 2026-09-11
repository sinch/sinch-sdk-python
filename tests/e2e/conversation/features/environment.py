from tests.e2e.shared_config import create_test_client

NOT_IMPLEMENTED_SCENARIOS = {}


def before_all(context):
    """Initializes the Sinch client"""
    context.sinch = create_test_client()


def before_scenario(context, scenario):
    """Skips the scenarios covering operations this SDK does not implement yet."""
    if scenario.name in NOT_IMPLEMENTED_SCENARIOS:
        scenario.skip("SDK operation not implemented yet")
