from typing import Optional, List
from sinch.domains.number_lookup.api.v1.base import BaseLookup
from sinch.domains.number_lookup.api.v1.internal import LookupNumberEndpoint
from sinch.domains.number_lookup.models.v1.internal import LookupNumberRequest
from sinch.domains.number_lookup.models.v1.response import LookupNumberResponse
from sinch.domains.number_lookup.models.v1.types import RndFeatureOptionsDict


class NumberLookup(BaseLookup):
    def lookup(
        self,
        number: str,
        features: Optional[List[str]] = None,
        rnd_feature_options: Optional[RndFeatureOptionsDict] = None,
        **kwargs,
    ) -> LookupNumberResponse:
        """
        Performs a number lookup.
        You can make a minimal request or add additional options to the features array.

        :param number: MSISDN in E.164 format to query (e.g., "+12312312312")
        :type number: str
        :param features: List of requested features. Options: "LineType", "SimSwap", "VoIPDetection", "RND"
        :type features: Optional[List[str]]
        :param rnd_feature_options: Optional dictionary with RND feature options
        :type rnd_feature_options: Optional[RndFeatureOptionsDict]
        :param **kwargs: Additional parameters for the request.
        :type **kwargs: dict

        :returns: LookupNumberResponse
        :rtype: LookupNumberResponse
        """
        request_data = LookupNumberRequest(
            number=number,
            features=features,
            rnd_feature_options=rnd_feature_options,
            **kwargs,
        )
        return self._request(LookupNumberEndpoint, request_data)
