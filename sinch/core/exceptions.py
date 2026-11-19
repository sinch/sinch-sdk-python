class SinchException(Exception):
    def __init__(self, message, response, is_from_server):
        self.is_from_server = is_from_server
        status = getattr(response, "status", None)
        if status is None:
            status = getattr(response, "status_code", None)
        self.response_status_code = status
        self.http_response = response
        super().__init__(message)


class ValidationException(SinchException):
    pass
