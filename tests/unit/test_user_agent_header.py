from platform import python_version
from sinch import __version__ as sdk_version
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.core.models.http_response import HTTPResponse


class DummyEndpoint(HTTPEndpoint):
    """Dummy endpoint for testing core functionality"""

    ENDPOINT_URL = "https://capy.sinch.com/v1/test"

    @property
    def HTTP_METHOD(self) -> str:
        return HTTPMethods.GET.value

    @property
    def HTTP_AUTHENTICATION(self) -> str:
        return HTTPAuthentication.OAUTH.value

    def build_url(self, sinch):
        return self.ENDPOINT_URL

    def build_query_params(self):
        return {}

    def request_body(self):
        return ""

    def handle_response(self, response: HTTPResponse):
        return response


def test_user_agent_header_creation_expects_to_be_included(sinch_client_sync):
    """
    Test that User-Agent header is created with the correct format.

    Expected format: sinch-sdk/{sdk_version} (Python/{python_version}; {implementation_type}; {auxiliary_flag})
    Note: auxiliary_flag is currently always empty in the implementation.
    """
    endpoint = DummyEndpoint("dummy_project_id", {})
    http_request = sinch_client_sync.configuration.transport.prepare_request(endpoint)

    assert "User-Agent" in http_request.headers

    user_agent = http_request.headers["User-Agent"]
    transport_class_name = sinch_client_sync.configuration.transport.__class__.__name__

    # Parse the User-Agent string
    prefix, info_section = user_agent.split(" (", 1)
    info_section = info_section.rstrip(")")
    components = [c.strip() for c in info_section.split(";")]

    # Validate structure
    assert prefix == f"sinch-sdk/{sdk_version}", f"Expected prefix 'sinch-sdk/{sdk_version}', got '{prefix}'"
    assert len(components) == 3, f"Expected 3 components, got {len(components)}: {components}"
    assert components[0] == f"Python/{python_version()}", f"Expected 'Python/{python_version()}', got '{components[0]}'"
    assert components[1] == transport_class_name, f"Expected '{transport_class_name}', got '{components[1]}'"
    assert components[2] == "", f"Auxiliary flag should be empty (not implemented yet), got '{components[2]}'"
