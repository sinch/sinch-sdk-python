class BaseVoice:
    """Base class for handling Sinch Voice operations."""

    def __init__(self, sinch):
        self._sinch = sinch

    def _request(self, endpoint_class, request_data):
        """
        A helper method to make requests to endpoints.

        :param endpoint_class: The endpoint class to call.
        :param request_data: The request data to pass to the endpoint.
        :returns: The response from the Sinch transport request.
        """
        return self._sinch.configuration.transport.request(
            endpoint_class(
                project_id=self._sinch.configuration.project_id,
                request_data=request_data,
            )
        )
