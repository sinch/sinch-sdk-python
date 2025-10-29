class BaseSms:
    """Base class for handling Sinch Sms operations."""

    def __init__(self, sinch):
        self._sinch = sinch

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

        # Use service_plan_id for SMS auth, project_id for project auth
        if self._sinch.configuration.authentication_method == "sms_auth":
            path_identifier = self._sinch.configuration.service_plan_id
        else:
            path_identifier = self._sinch.configuration.project_id

        endpoint = endpoint_class(
            project_id=path_identifier,
            request_data=request_data,
        )

        # Set the authentication method based on configuration
        endpoint.set_authentication_method(self._sinch)

        return self._sinch.configuration.transport.request(endpoint)
