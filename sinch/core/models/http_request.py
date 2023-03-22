from dataclasses import dataclass


@dataclass
class HttpRequest:
    headers: dict
    protocol: str
    url: str
    http_method: str
    request_body: dict
    query_params: dict
    auth: str
