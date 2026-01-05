import re
from abc import ABC
from typing import Type, Union, get_origin, get_args
from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.types import BM
from sinch.domains.conversation.api.v1.exceptions import ConversationException


class ConversationEndpoint(HTTPEndpoint, ABC):
    def __init__(self, project_id: str, request_data: BM):
        super().__init__(project_id, request_data)

    def build_url(self, sinch) -> str:
        if not self.ENDPOINT_URL:
            raise NotImplementedError(
                f"ENDPOINT_URL must be defined in the Conversation endpoint subclass "
                f"'{self.__class__.__name__}'."
            )

        # TODO: Add support and validation for conversation_region in SinchClient initialization;

        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.conversation_origin,
            project_id=self.project_id,
            **vars(self.request_data),
        )

    def _get_path_params_from_url(self) -> set:
        """
        Extracts path parameters from ENDPOINT_URL template.

        Returns:
            set: Set of path parameter names that should be excluded from request body and query params.
        """
        if not self.ENDPOINT_URL:
            return set()

        # Extract all placeholders from the URL template (e.g., {message_id}, {project_id})
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
            # Check if response_model is a Union type
            if origin is Union:
                # For Union types, try to validate against each type in the Union sequentially
                # This handles cases where TypeAdapter might not be fully defined
                union_args = get_args(response_model)
                last_error = None

                # Try each type in the Union until one succeeds
                for union_type in union_args:
                    try:
                        return union_type.model_validate(response_body)
                    except Exception as e:
                        last_error = e
                        continue

                # If all Union types failed, raise an error with the last error details
                if last_error is not None:
                    raise ValueError(
                        f"Invalid response structure: None of the Union types matched. "
                        f"Last error: {last_error}"
                    ) from last_error

            # Use standard model_validate for regular Pydantic models
            return response_model.model_validate(response_body)
        except Exception as e:
            raise ValueError(f"Invalid response structure: {e}") from e

    def handle_response(self, response: HTTPResponse):
        if response.status_code >= 400:
            raise ConversationException(
                message=f"{response.body['error'].get('message')}  {response.body['error'].get('status')}",
                response=response,
                is_from_server=True,
            )
