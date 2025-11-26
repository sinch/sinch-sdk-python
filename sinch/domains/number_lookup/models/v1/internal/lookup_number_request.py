from datetime import datetime, date
from typing import Optional, Dict, Any
from pydantic import Field, StrictStr, conlist, field_serializer
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
        if value is None:
            return None

        serialized = {}
        for key, val in value.items():
            if isinstance(val, (datetime, date)):
                # Convert datetime/date to ISO 8601 date format (YYYY-MM-DD)
                if isinstance(val, datetime):
                    serialized[key] = val.date().isoformat()
                else:
                    serialized[key] = val.isoformat()
            else:
                # Pass string values directly to the backend without modification
                serialized[key] = val
        return serialized
