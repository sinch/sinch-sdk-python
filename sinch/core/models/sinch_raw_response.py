"""Fallback variant for response union members the SDK does not recognize."""

from sinch.core.models.internal.base_model_config import BaseConfigModel

class SinchRawResponse(BaseConfigModel):
    """Returned in place of a union member when no declared variant matches. Only produced while parsing a response"""
