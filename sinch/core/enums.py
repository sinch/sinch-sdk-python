from enum import Enum


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PATCH = "PATCH"
    PUT = "PUT"


class HTTPAuthentication(Enum):
    BASIC = "BASIC"
    OAUTH = "OAUTH"
    SIGNED = "SIGNED"
