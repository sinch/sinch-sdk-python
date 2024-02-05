from dataclasses import dataclass

from sinch.core.models.base_model import SinchRequestBaseModel, SinchBaseModel


@dataclass
class TokenPaginatedRequest(SinchRequestBaseModel):
    page_token: str


@dataclass
class IntPaginatedRequest(SinchRequestBaseModel):
    page: int
    page_size: int


@dataclass
class TokenPaginatedResponse(SinchBaseModel):
    next_page_token: str


@dataclass
class IntPaginatedResponse(SinchBaseModel):
    page: int
    page_size: int
