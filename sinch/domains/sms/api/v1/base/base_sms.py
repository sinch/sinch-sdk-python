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
        return self._sinch.configuration.transport.request(
            endpoint_class(
                # TODO: Refactor project_id to service_plan_id
                project_id=self._sinch.configuration.project_id,
                request_data=request_data,
            )
        )
