from dataclasses import dataclass
from typing import Optional


@dataclass
class HttpRequest:
    headers: dict
    protocol: str
    url: str
    http_method: str
    request_body: dict
    query_params: dict
    auth: Optional[tuple[str, str]]
