class BaseSms:
    """Base class for handling Sinch Sms operations."""

    def __init__(self, sinch):
        self._sinch = sinch

    def _get_path_identifier(self) -> str:
        """
        Returns the appropriate path identifier based on authentication method.
        - SMS auth: returns service_plan_id
        - Project auth: returns project_id

        Returns:
            str: The path identifier to use for the endpoint.
        """
        if self._sinch.configuration.authentication_method == "sms_auth":
            return self._sinch.configuration.service_plan_id
        else:
            return self._sinch.configuration.project_id

    def _request(self, endpoint_class, request_data):
        """
        A helper method to make requests to endpoints.

        Args:
            endpoint_class: The endpoint class to call.
            request_data: The request data to pass to the endpoint.

        Returns:
            The response from the Sinch transport request.
        """
        self._sinch.configuration.validate_authentication_parameters()

        endpoint = endpoint_class(
            project_id=self._get_path_identifier(),
            request_data=request_data,
        )

        # Set the authentication method based on configuration
        endpoint.set_authentication_method(self._sinch)

        return self._sinch.configuration.transport.request(endpoint)
