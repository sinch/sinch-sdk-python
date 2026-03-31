from dataclasses import dataclass


@dataclass
class HTTPResponse:
    status_code: int
    headers: dict
    body: dict = None
