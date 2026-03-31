from pydantic import BaseModel, Field, StrictStr


class BatchIdMixin(BaseModel):
    """Mixin that adds batch_id field to request models."""

    batch_id: StrictStr = Field(
        default=...,
        description="The batch ID you received from sending a message.",
    )
