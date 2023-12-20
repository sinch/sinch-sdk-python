import hashlib
import hmac
import base64
from datetime import datetime, timezone


class Signature:
    def __init__(self, sinch, http_method, request_data, request_uri):
        self.sinch = sinch
        self.http_method = http_method
        self.content_type = 'application/json; charset=UTF-8'
        self.request_data = request_data
        self.signature_time = datetime.now(timezone.utc).isoformat()
        self.request_uri = request_uri
        self.authorization_signature = None

    def get_http_headers_with_signature(self):
        if not self.authorization_signature:
            self.calculate()

        return {
            "Content-Type": self.content_type,
            "Authorization": (
                f"Application {self.sinch.configuration.verification_key}:{self.authorization_signature}"
            ),
            "x-timestamp": self.signature_time
        }

    def calculate(self):
        b64_encoded_application_secret = base64.b64decode(self.sinch.configuration.verification_secret)
        if self.request_data:
            encoded_verification_request = hashlib.md5(self.request_data.encode())
            encoded_verification_request = base64.b64encode(encoded_verification_request.digest())

        else:
            encoded_verification_request = ''.encode()

        request_timestamp = "x-timestamp:" + self.signature_time

        string_to_sign = (
            self.http_method + '\n'
            + encoded_verification_request.decode() + '\n'
            + self.content_type + '\n'
            + request_timestamp + '\n'
            + self.request_uri
        )

        self.authorization_signature = base64.b64encode(
            hmac.new(b64_encoded_application_secret, string_to_sign.encode(), hashlib.sha256).digest()
        ).decode()