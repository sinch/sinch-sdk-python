from typing import Optional, List, Dict
from pydantic import Field, StrictStr
from sinch.domains.number_lookup.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class LookupNumberRequest(BaseModelConfigurationRequest):
    number: StrictStr = Field(
        ..., description="MSISDN in E.164 format to query"
    )
    features: Optional[List[str]] = Field(
        default=None,
        description="Contains requested features. Fallback to LineType if not provided.",
    )
    rnd_feature_options: Optional[Dict] = Field(
        default=None, alias="rndFeatureOptions"
    )
