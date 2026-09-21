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
    SMS_TOKEN = "SMS_TOKEN"


class VoiceRegionEnum(str, Enum):
    GLOBAL = ""
    NORTH_AMERICA = "us1"
    SOUTH_AMERICA = "br1"
    EUROPE = "eu1"
    ASIA_PACIFIC = "sg1"
    AUSTRALIA = "au1"

    
class RetryPolicy(Enum):
    #: Honor a ``Retry-After`` header if present, otherwise fall back to backoff.
    DEFAULT = "DEFAULT"
    #: Retry only when a ``Retry-After`` header is present; give up otherwise.
    RETRY_AFTER = "RETRY_AFTER"
    #: Always use exponential backoff, ignoring any ``Retry-After`` header.
    BACKOFF = "BACKOFF"
    #: Never retry rate-limited requests.
    NONE = "NONE"
