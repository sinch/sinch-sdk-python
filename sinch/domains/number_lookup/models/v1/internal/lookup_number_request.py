from typing import Optional, Dict, Any
from pydantic import Field, StrictStr, conlist, field_serializer
from sinch.core.models.utils import serialize_datetime_in_dict
from sinch.domains.number_lookup.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)
from sinch.domains.number_lookup.models.v1.types import LookupFeaturesType


class LookupNumberRequest(BaseModelConfigurationRequest):
    number: StrictStr = Field(
        ..., description="MSISDN in E.164 format to query"
    )
    features: Optional[conlist(LookupFeaturesType)] = Field(
        default=None,
        description="Contains requested features. Fallback to LineType if not provided.",
    )
    rnd_feature_options: Optional[Dict[str, Any]] = Field(
        default=None, alias="rndFeatureOptions"
    )

    @field_serializer("rnd_feature_options")
    def serialize_rnd_feature_options(
        self, value: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        return serialize_datetime_in_dict(value)
