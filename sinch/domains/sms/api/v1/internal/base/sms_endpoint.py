import re
from abc import ABC
from typing import Annotated, Type, Union, get_origin, get_args
from pydantic import TypeAdapter
from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.types import BM
from sinch.core.enums import HTTPAuthentication
from sinch.domains.sms.api.v1.exceptions import SmsException


class SmsEndpoint(HTTPEndpoint, ABC):
    def __init__(self, project_id: str, request_data: BM):
        super().__init__(project_id, request_data)

    def set_authentication_method(self, sinch):
        """
        Sets the authentication method based on the sinch client configuration.
        """
        if sinch.configuration.authentication_method == "sms_auth":
            self.HTTP_AUTHENTICATION = HTTPAuthentication.SMS_TOKEN.value
        else:
            self.HTTP_AUTHENTICATION = HTTPAuthentication.OAUTH.value

    def build_url(self, sinch) -> str:
        if not self.ENDPOINT_URL:
            raise NotImplementedError(
                "ENDPOINT_URL must be defined in the subclass."
            )

        # Use the appropriate SMS origin based on authentication method
        origin = sinch.configuration.get_sms_origin_for_auth()

        return self.ENDPOINT_URL.format(
            origin=origin,
            project_id=self.project_id,
            **vars(self.request_data),
        )

    def _get_path_params_from_url(self) -> set:
        """
        Extracts path parameters from ENDPOINT_URL template.

        Returns:
            set: Set of path parameter names that should be excluded from request body.
        """
        if not self.ENDPOINT_URL:
            return set()

        # Extract all placeholders from the URL template (e.g., {batch_id}, {project_id})
        path_params = set(re.findall(r"\{(\w+)\}", self.ENDPOINT_URL))

        # Exclude 'origin' and 'project_id' as they are always path params but not from request_data
        path_params.discard("origin")
        path_params.discard("project_id")

        return path_params

    def build_query_params(self) -> dict:
        """
        Constructs the query parameters for the endpoint.

        Returns:
            dict: The query parameters to be sent with the API request.
        """
        return {}

    def request_body(self) -> str:
        """
        Returns the request body as a JSON string.

        Returns:
            str: The request body as a JSON string.
        """
        return ""

    def process_response_model(
        self, response_body: dict, response_model: Type[BM]
    ) -> BM:
        """
        Processes the response body and maps it to a response model.

        Args:
            response_body (dict): The raw response body.
            response_model (type): The Pydantic model class or Union type to map the response.

        Returns:
            Parsed response object.
        """
        try:
            origin = get_origin(response_model)
            # Check if response_model is an Annotated type (e.g., discriminated union)
            if origin is Annotated:
                args = get_args(response_model)
                if args and get_origin(args[0]) is Union:
                    # Use TypeAdapter for Annotated Union types (discriminated unions)
                    adapter = TypeAdapter(response_model)
                    return adapter.validate_python(response_body)
            # Check if response_model is a Union type
            elif origin is Union:
                # Use TypeAdapter for Union types
                adapter = TypeAdapter(response_model)
                return adapter.validate_python(response_body)
            # Use standard model_validate for regular Pydantic models
            return response_model.model_validate(response_body)
        except Exception as e:
            raise ValueError(f"Invalid response structure: {e}") from e

    def handle_response(self, response: HTTPResponse):
        if response.status_code >= 400:
            error_message = f"Error {response.status_code}"

            raise SmsException(
                message=error_message,
                response=response,
                is_from_server=True,
            )
