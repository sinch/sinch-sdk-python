from pydantic import BaseModel, Field, StrictStr


class GroupIdMixin(BaseModel):
    """Mixin that adds group_id field to request models."""

    group_id: StrictStr = Field(
        default=...,
        description="ID of the group.",
    )
