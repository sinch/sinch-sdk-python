from abc import ABC
from typing import Type
from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.core.types import BM
from sinch.core.enums import HTTPAuthentication


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
        if response.status_code >= 400:
            print(response.body)
            # raise SmsException(
            #     message=f"{response.body['error'].get('message')}  {response.body['error'].get('status')}",
            #     response=response,
            #     is_from_server=True,
            # )
