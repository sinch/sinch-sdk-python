from dataclasses import dataclass


@dataclass
class HTTPResponse:
    status_code: int
    body: dict
    headers: dict
