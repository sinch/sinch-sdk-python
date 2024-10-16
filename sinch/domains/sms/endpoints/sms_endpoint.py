from sinch.core.models.http_response import HTTPResponse
from sinch.core.endpoint import HTTPEndpoint
from sinch.domains.sms.exceptions import SMSException
from sinch.core.enums import HTTPAuthentication


class SMSEndpoint(HTTPEndpoint):
    def __init__(self, request_data, sinch):
        self.request_data = request_data
        self.sinch = sinch

        if sinch.configuration.sms_authentication_method == HTTPAuthentication.OAUTH.value:
            self.project_or_service_id = sinch.configuration.project_id
            self.sms_origin = self.sinch.configuration.sms_origin

        elif sinch.configuration.sms_authentication_method == HTTPAuthentication.SMS_TOKEN.value:
            self.project_or_service_id = sinch.configuration.service_plan_id
            self.HTTP_AUTHENTICATION = HTTPAuthentication.SMS_TOKEN.value
            self.sms_origin = self.sinch.configuration._sms_origin_with_service_plan_id

    def handle_response(self, response: HTTPResponse):
        if response.status_code >= 400:
            raise SMSException(
                message=response.body["text"],
                response=response,
                is_from_server=True
            )
