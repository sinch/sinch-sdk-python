import json
from pydantic import BaseModel
from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.domains.numbers.exceptions import NumbersException


class NumbersEndpoint(HTTPEndpoint):
    """
        A base class for all endpoints, providing reusable logic for URL building
        and response parsing.
        """
    ENDPOINT_URL: str = ""
    HTTP_METHOD: str = ""
    HTTP_AUTHENTICATION: str = ""

    def __init__(self, project_id: str, request_data: object):
        self.project_id = project_id
        self.request_data = request_data

    def build_url(self, sinch) -> str:
        """
        Constructs the URL for the endpoint.

        Args:
            sinch: The Sinch client instance.

        Returns:
            str: Fully constructed endpoint URL.
        """
        if not self.ENDPOINT_URL:
            raise NotImplementedError("ENDPOINT_URL must be defined in the subclass.")

        return self.ENDPOINT_URL.format(
            origin=sinch.configuration.numbers_origin,
            project_id=self.project_id,
            **vars(self.request_data)
        )

    def request_body(self):
        """
        Returns the request body as a JSON string.

        Returns:
            str: The request body as a JSON string.
        """
        # Convert the request data to a dictionary and remove None values
        request_data = self.request_data.model_dump(by_alias=True, exclude_none=True)
        return json.dumps(request_data)

    def process_response_model(self, response_body: dict, response_model: type[BaseModel]) -> BaseModel:
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
        if response.status_code >= 400:
            raise NumbersException(
                message=f"{response.body['error'].get('message')}  {response.body['error'].get('status')}",
                response=response,
                is_from_server=True
            )
