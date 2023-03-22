from dataclasses import dataclass
from sinch.core.models.base_model import SinchBaseModel


@dataclass
class OAuthToken(SinchBaseModel):
    access_token: str
    expires_in: int
    scope: str
    token_type: str
