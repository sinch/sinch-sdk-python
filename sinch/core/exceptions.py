class SinchException(Exception):
    def __init__(self, message: str, response, is_from_server: str):
        self.is_from_server = is_from_server
        self.response_status_code = response.status_code if response else None
        self.http_response = response
        super().__init__(message)


class ValidationException(SinchException):
    pass
