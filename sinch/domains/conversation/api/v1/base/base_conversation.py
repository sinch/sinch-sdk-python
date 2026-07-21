class BaseConversation:
    """Base class for handling Sinch Conversation operations."""

    def __init__(self, sinch):
        self._sinch = sinch

    def _request(self, endpoint_class, request_data, response_model=None):
        """
        A helper method to make requests to endpoints.

        Args:
            endpoint_class: The endpoint class to call.
            request_data: The request data to pass to the endpoint.
            response_model: Optional Pydantic model to deserialize the response into.
                When provided, it is forwarded to the endpoint constructor.

        Returns:
            The response from the Sinch transport request.
        """
        endpoint_kwargs = {
            "project_id": self._sinch.configuration.project_id,
            "request_data": request_data,
        }
        if response_model is not None:
            endpoint_kwargs["response_model"] = response_model
        return self._sinch.configuration.transport.request(
            endpoint_class(**endpoint_kwargs)
        )
