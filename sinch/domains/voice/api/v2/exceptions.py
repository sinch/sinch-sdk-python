from sinch.core.exceptions import SinchException


class VoiceException(SinchException):
    def __init__(
        self,
        message,
        response,
        is_from_server,
        error_type=None,
        instance=None,
    ):
        super().__init__(message, response, is_from_server)
        self.error_type = error_type
        self.instance = instance
