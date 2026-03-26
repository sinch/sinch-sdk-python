import re
from abc import ABC
from typing import Type
from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.types import BM
from sinch.domains.numbers.api.v1.exceptions import NumbersException
from sinch.domains.numbers.models.v1.errors import NotFoundError


class NumbersEndpoint(HTTPEndpoint, ABC):
    def __init__(self, project_id: str, request_data: BM):
        super().__init__(project_id, request_data)

    def build_url(self, sinch) -> str:
        if not self.ENDPOINT_URL:
            raise NotImplementedError(
                "ENDPOINT_URL must be defined in the Numbers endpoint subclass "
            )

        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id,
            **vars(self.request_data),
        )

    def _get_path_params_from_url(self) -> set:
        """
        Extracts path parameters from ENDPOINT_URL template.

        Returns:
            set: Set of path parameter names that should be excluded
                 from request body and query params.
        """
        if not self.ENDPOINT_URL:
            return set()

        path_params = set(re.findall(r"\{(\w+)\}", self.ENDPOINT_URL))
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
            response_model (type): The Pydantic model class to map the response.

        Returns:
            Parsed response object.
        """
        try:
            return response_model.model_validate(response_body)
        except Exception as e:
            raise ValueError(f"Invalid response structure: {e}") from e

    def handle_response(self, response: HTTPResponse):
        error_data = (response.body or {}).get("error", {})

        if response.status_code == 404:
            try:
                error = NotFoundError(**error_data)
            except TypeError:
                error = f"Not found: {error_data}"
            raise NumbersException(
                message=error, response=response, is_from_server=True
            )

        if response.status_code >= 400:
            message = error_data.get('message', '')
            status = error_data.get('status', '')
            error_message = f"{message}  {status}".strip() or f"Error {response.status_code}"
            raise NumbersException(
                message=error_message,
                response=response,
                is_from_server=True,
            )
