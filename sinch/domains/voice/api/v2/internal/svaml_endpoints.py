from sinch.core.enums import HTTPAuthentication, HTTPMethods
from sinch.domains.voice.api.v2.internal.base.voice_endpoint import (
    VoiceEndpoint,
)
from sinch.domains.voice.models.v2.svaml.internal.request.describe_svaml_request import (
    DescribeSvamlRequest,
)
from sinch.domains.voice.models.v2.svaml.internal.request.validate_svaml_request import (
    ValidateSvamlRequest,
)
from sinch.domains.voice.models.v2.svaml.response.describe_svaml_response import (
    DescribeSvamlResponse,
)
from sinch.domains.voice.models.v2.svaml.response.validate_svaml_response import (
    ValidateSvamlResponse,
)


class DescribeSvamlEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/svaml/describe"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: DescribeSvamlRequest,
        response_model=DescribeSvamlResponse,
    ):
        super().__init__(project_id, request_data, response_model)


class ValidateSvamlEndpoint(VoiceEndpoint):
    ENDPOINT_URL = "{origin}/v2/projects/{project_id}/svaml/validate"
    HTTP_METHOD = HTTPMethods.POST.value
    HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def __init__(
        self,
        project_id: str,
        request_data: ValidateSvamlRequest,
        response_model=ValidateSvamlResponse,
    ):
        super().__init__(project_id, request_data, response_model)
