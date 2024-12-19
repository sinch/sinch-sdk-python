from enum import Enum


class HTTPMethods(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PATCH = "PATCH"
    PUT = "PUT"


class HTTPAuthentication(Enum):
    BASIC = "BASIC"
    OAUTH = "OAUTH"
    SIGNED = "SIGNED"
    SMS_TOKEN = "SMS_TOKEN"
