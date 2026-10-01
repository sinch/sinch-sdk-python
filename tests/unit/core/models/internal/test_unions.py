"""Tests for the union resolution shared by every ``oneOf``-derived union.

Covers the four shapes of ``oneOf`` the SDK maps, in both directions:

1. a closed discriminator, every member pinning its own ``Literal`` value;
2. an open discriminator, with a member absorbing the unknown values;
3. no discriminator, members told apart by which marker field is present;
4. no discriminator, members overlapping and told apart by validation.

The request policy rejects what it cannot resolve; the response policy falls
back, so a variant the API adds later stays parseable.
"""

from typing import Annotated, Dict, List, Literal, Optional, Union, get_args

import warnings

import pytest
from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    StrictStr,
    TypeAdapter,
    ValidationError,
)

from sinch.core.models.internal.base_model_config import BaseConfigModel
from sinch.core.models.internal.unions import (
    ResolveUnion,
    _resolve,
    response_parsing_scope,
)
from sinch.core.models.sinch_raw_response import SinchRawResponse


# ---------------------------------------------------------------------------
# Type 1 and 2: discriminated members
# ---------------------------------------------------------------------------


class RTCConfig(BaseConfigModel):
    type: Literal["RTC"] = "RTC"
    app_id: Optional[StrictStr] = Field(default=None, alias="appId")


class ESTConfig(BaseConfigModel):
    type: Literal["EST"] = "EST"
    trunk_id: Optional[StrictStr] = Field(default=None, alias="trunkId")


class CustomConfig(BaseConfigModel):
    type: StrictStr


class ChannelCredentials(BaseConfigModel):
    channel: StrictStr


class BearerCredentials(ChannelCredentials):
    bearer_token: StrictStr


class TokenCredentials(ChannelCredentials):
    static_token: StrictStr


ClosedRequest = Annotated[
    Union[
        RTCConfig,
        ESTConfig,
    ],
    ResolveUnion(discriminator="type"),
]
ClosedResponse = Annotated[
    Union[
        RTCConfig,
        ESTConfig,
    ],
    ResolveUnion(discriminator="type"),
]
OpenResponse = Annotated[
    Union[
        RTCConfig,
        ESTConfig,
        CustomConfig,
    ],
    ResolveUnion(discriminator="type", fallback=CustomConfig),
]


# ---------------------------------------------------------------------------
# Type 3: members told apart by a marker field
# ---------------------------------------------------------------------------


class Coordinates(BaseConfigModel):
    latitude: float
    longitude: float


class TextContent(BaseConfigModel):
    text_message: Optional[Dict[str, StrictStr]] = None


class LocationContent(BaseConfigModel):
    location_message: Optional[Coordinates] = None


class MediaContent(BaseConfigModel):
    media_message: Optional[Dict[str, StrictStr]] = None


MarkerRequest = Annotated[
    Union[
        TextContent,
        LocationContent,
        MediaContent,
    ],
    ResolveUnion(),
]
MarkerResponse = Annotated[
    Union[
        TextContent,
        LocationContent,
        MediaContent,
    ],
    ResolveUnion(),
]


# ---------------------------------------------------------------------------
# Type 4: overlapping members, told apart by validation
# ---------------------------------------------------------------------------


class TextBatch(BaseConfigModel):
    to: List[StrictStr]
    body: StrictStr


class BinaryBatch(BaseConfigModel):
    to: List[StrictStr]
    body: StrictStr
    udh: StrictStr


class MediaBatch(BaseConfigModel):
    to: List[StrictStr]
    body: Dict[str, StrictStr]


OverlappingRequest = Annotated[
    Union[
        TextBatch,
        BinaryBatch,
        MediaBatch,
    ],
    ResolveUnion(),
]
OverlappingResponse = Annotated[
    Union[
        TextBatch,
        BinaryBatch,
        MediaBatch,
    ],
    ResolveUnion(),
]


def resolve(union, payload, parsing_response=False):
    """Validates a payload against a union, optionally as a response body."""
    adapter = TypeAdapter(union)
    if parsing_response:
        with response_parsing_scope():
            return adapter.validate_python(payload)
    return adapter.validate_python(payload)


# ---------------------------------------------------------------------------
# Type 1: closed discriminator
# ---------------------------------------------------------------------------


class TestClosedDiscriminator:
    @pytest.mark.parametrize(
        "payload, expected",
        [
            ({"type": "RTC", "appId": "app-1"}, RTCConfig),
            ({"type": "EST", "trunkId": "trunk-1"}, ESTConfig),
        ],
        ids=["rtc", "est"],
    )
    def test_known_tag_resolves_to_its_member_in_a_request(
        self, payload, expected
    ):
        assert type(resolve(ClosedRequest, payload)) is expected

    @pytest.mark.parametrize(
        "payload, expected",
        [
            ({"type": "RTC", "appId": "app-1"}, RTCConfig),
            ({"type": "EST", "trunkId": "trunk-1"}, ESTConfig),
        ],
        ids=["rtc", "est"],
    )
    def test_known_tag_resolves_to_its_member_in_a_response(
        self, payload, expected
    ):
        resolved = resolve(ClosedResponse, payload, parsing_response=True)
        assert type(resolved) is expected

    def test_unknown_tag_is_rejected_in_a_request(self):
        with pytest.raises(ValidationError) as excinfo:
            resolve(ClosedRequest, {"type": "WEBRTC_V2", "appId": "app-1"})

        assert excinfo.value.errors()[0]["type"] == "union_tag_invalid"

    def test_missing_tag_is_rejected_in_a_request(self):
        with pytest.raises(ValidationError) as excinfo:
            resolve(ClosedRequest, {"appId": "app-1"})

        assert excinfo.value.errors()[0]["type"] == "union_tag_not_found"

    def test_unknown_tag_resolves_to_unknown_in_a_response(self):
        payload = {"type": "WEBRTC_V2", "appId": "app-1"}
        resolved = resolve(ClosedResponse, payload, parsing_response=True)

        assert isinstance(resolved, SinchRawResponse)
        assert resolved.model_dump() == payload

    def test_missing_tag_resolves_to_unknown_in_a_response(self):
        resolved = resolve(
            ClosedResponse, {"appId": "app-1"}, parsing_response=True
        )
        assert isinstance(resolved, SinchRawResponse)

    def test_tags_are_matched_case_sensitively(self):
        resolved = resolve(
            ClosedResponse, {"type": "rtc"}, parsing_response=True
        )
        assert isinstance(resolved, SinchRawResponse)

    def test_tag_is_read_from_the_alias_casing_too(self):
        class CamelTagged(BaseConfigModel):
            message_type: Literal["TEXT"] = Field(
                default="TEXT", alias="messageType"
            )

        union = Annotated[
            Union[
                CamelTagged,
            ],
            ResolveUnion(discriminator="message_type"),
        ]
        resolved = resolve(union, {"messageType": "TEXT"}, True)

        assert type(resolved) is CamelTagged

    def test_invalid_payload_under_a_known_tag_raises_in_a_request(self):
        with pytest.raises(ValidationError):
            resolve(ClosedRequest, {"type": "RTC", "appId": 42})

    def test_invalid_payload_under_a_known_tag_is_unknown_in_a_response(self):
        resolved = resolve(
            ClosedResponse, {"type": "RTC", "appId": 42}, parsing_response=True
        )
        assert isinstance(resolved, SinchRawResponse)


# ---------------------------------------------------------------------------
# Type 2: open discriminator with a fallback member
# ---------------------------------------------------------------------------


class TestOpenDiscriminator:
    def test_unknown_tag_resolves_to_the_declared_fallback(self):
        payload = {"type": "WEBRTC_V2", "newField": 1}
        resolved = resolve(OpenResponse, payload, parsing_response=True)

        assert type(resolved) is CustomConfig
        assert resolved.type == "WEBRTC_V2"

    def test_payload_the_fallback_rejects_resolves_to_unknown(self):
        resolved = resolve(
            OpenResponse, {"appId": "app-1"}, parsing_response=True
        )
        assert isinstance(resolved, SinchRawResponse)

    def test_declared_fallback_absorbs_an_unknown_tag_in_a_request_too(self):
        union = Annotated[
            Union[
                RTCConfig,
                ESTConfig,
                CustomConfig,
            ],
            ResolveUnion(discriminator="type", fallback=CustomConfig),
        ]
        resolved = resolve(union, {"type": "WEBRTC_V2"})

        assert type(resolved) is CustomConfig

    def test_invalid_payload_under_a_known_tag_raises_despite_the_fallback_in_a_request(
        self,
    ):
        union = Annotated[
            Union[
                RTCConfig,
                ESTConfig,
                CustomConfig,
            ],
            ResolveUnion(discriminator="type", fallback=CustomConfig),
        ]
        with pytest.raises(ValidationError, match="app_id|appId"):
            resolve(union, {"type": "RTC", "appId": 42})

    def test_invalid_payload_under_a_known_tag_resolves_to_the_fallback_in_a_response(
        self,
    ):
        resolved = resolve(
            OpenResponse, {"type": "RTC", "appId": 42}, parsing_response=True
        )
        assert type(resolved) is CustomConfig

    def test_request_without_a_declared_fallback_rejects_an_unknown_tag(self):
        with pytest.raises(ValidationError, match="does not match any of the expected tags"):
            resolve(ClosedRequest, {"type": "WEBRTC_V2"})

    def test_known_tag_still_wins_over_the_fallback(self):
        resolved = resolve(
            OpenResponse, {"type": "RTC", "appId": "a"}, parsing_response=True
        )
        assert type(resolved) is RTCConfig

    def test_explicit_tags_map_several_values_to_one_member(self):
        union = Annotated[
            Union[
                BearerCredentials,
                TokenCredentials,
            ],
            ResolveUnion(
                discriminator="channel",
                tags={
                        "WHATSAPP": BearerCredentials,
                        "RCS": BearerCredentials,
                        "MESSENGER": TokenCredentials,
                    },
            ),
        ]
        payload = {"channel": "RCS", "bearer_token": "secret"}
        resolved = resolve(union, payload, parsing_response=True)

        assert type(resolved) is BearerCredentials

    def test_explicit_tags_try_each_candidate_of_one_value_in_order(self):
        union = Annotated[
            Union[
                BearerCredentials,
                TokenCredentials,
            ],
            ResolveUnion(
                discriminator="channel",
                tags={"LINE": (BearerCredentials, TokenCredentials)},
            ),
        ]
        payload = {"channel": "LINE", "static_token": "secret"}
        resolved = resolve(union, payload, parsing_response=True)

        assert type(resolved) is TokenCredentials


# ---------------------------------------------------------------------------
# Type 3: marker fields
# ---------------------------------------------------------------------------


class TestMarkerFields:
    @pytest.mark.parametrize(
        "payload, expected",
        [
            ({"text_message": {"text": "hi"}}, TextContent),
            (
                {"location_message": {"latitude": 1.0, "longitude": 2.0}},
                LocationContent,
            ),
            ({"media_message": {"url": "https://x/y.jpg"}}, MediaContent),
        ],
        ids=["text", "location", "media"],
    )
    def test_marker_selects_its_member_whatever_the_declaration_order(
        self, payload, expected
    ):
        assert type(resolve(MarkerRequest, payload)) is expected

    def test_unknown_marker_resolves_to_the_first_member_in_a_response(self):
        payload = {"reaction_message": {"emoji": "x"}}
        resolved = resolve(MarkerResponse, payload, parsing_response=True)

        assert type(resolved) is TextContent
        assert resolved.reaction_message == {"emoji": "x"}

    def test_payload_without_any_marker_resolves_to_the_first_member_in_a_response(
        self,
    ):
        assert type(resolve(MarkerResponse, {}, parsing_response=True)) is TextContent

    def test_known_marker_carrying_an_invalid_value_is_unknown_in_a_response(
        self,
    ):
        payload = {"location_message": {"latitude": 1.0}}
        resolved = resolve(MarkerResponse, payload, parsing_response=True)

        assert isinstance(resolved, SinchRawResponse)
        assert resolved.model_dump() == payload

    def test_two_markers_are_broken_by_declaration_order(self):
        payload = {
            "media_message": {"url": "u"},
            "text_message": {"text": "hi"},
        }
        assert type(resolve(MarkerRequest, payload)) is TextContent

    def test_extra_fields_do_not_change_the_resolved_member(self):
        payload = {"text_message": {"text": "hi"}, "beta_flag": True}
        resolved = resolve(MarkerResponse, payload, parsing_response=True)

        assert type(resolved) is TextContent
        assert resolved.beta_flag is True


# ---------------------------------------------------------------------------
# Type 4: overlapping members
# ---------------------------------------------------------------------------


class TestOverlappingMembers:
    def test_member_declaring_the_extra_field_wins(self):
        payload = {"to": ["+1"], "body": "AAA", "udh": "0605"}
        assert type(resolve(OverlappingRequest, payload)) is BinaryBatch

    def test_tied_members_are_told_apart_by_validating_them(self):
        payload = {"to": ["+1"], "body": {"url": "https://x/y.jpg"}}
        assert type(resolve(OverlappingRequest, payload)) is MediaBatch

    def test_tied_members_that_all_validate_keep_declaration_order(self):
        payload = {"to": ["+1"], "body": "hello"}
        assert type(resolve(OverlappingRequest, payload)) is TextBatch

    def test_key_holding_none_does_not_point_at_its_member(self):
        union, marker = get_args(OverlappingRequest)
        payload = {"to": ["+1"], "body": "hello", "udh": None}

        assert type(_resolve(payload, marker.spec_for(union))) is TextBatch

    def test_payload_matching_no_member_raises_the_union_error(self):
        with pytest.raises(ValidationError) as excinfo:
            resolve(OverlappingRequest, {"to": ["+1"]})

        assert "body" in str(excinfo.value)

    def test_payload_matching_no_member_resolves_to_unknown_in_a_response(
        self,
    ):
        resolved = resolve(
            OverlappingResponse, {"to": ["+1"]}, parsing_response=True
        )
        assert isinstance(resolved, SinchRawResponse)


# ---------------------------------------------------------------------------
# Resolution mechanics shared by every union
# ---------------------------------------------------------------------------


class TestResolutionMechanics:
    def test_an_already_built_member_keeps_its_class(self):
        instance = ESTConfig(trunk_id="trunk-1")
        assert resolve(ClosedRequest, instance) is not None
        assert type(resolve(ClosedRequest, instance)) is ESTConfig

    def test_a_non_mapping_value_is_left_to_pydantic(self):
        with pytest.raises(ValidationError):
            resolve(ClosedRequest, "not-a-mapping")

    def test_each_item_of_a_list_is_resolved_on_its_own(self):
        class Holder(BaseModel):
            items: List[MarkerResponse]

        payload = {
            "items": [
                {"text_message": {"text": "hi"}},
                {"media_message": {"url": "u"}},
                {"location_message": {"latitude": 1.0}},
            ]
        }
        with response_parsing_scope():
            holder = Holder.model_validate(payload)

        assert [type(item) for item in holder.items] == [
            TextContent,
            MediaContent,
            SinchRawResponse,
        ]

    def test_a_before_validator_declared_after_the_marker_runs_first(self):
        def default_to_rtc(payload):
            if not payload.get("type"):
                return {**payload, "type": "RTC"}
            return payload

        union = Annotated[
            Union[
                RTCConfig,
                ESTConfig,
            ],
            ResolveUnion(discriminator="type"),
            BeforeValidator(default_to_rtc),
        ]
        assert type(resolve(union, {"appId": "app-1"})) is RTCConfig

    def test_the_response_policy_does_not_leak_out_of_its_scope(self):
        with response_parsing_scope():
            pass

        with pytest.raises(ValidationError):
            resolve(ClosedRequest, {"type": "WEBRTC_V2"})

    def test_unknown_keeps_the_payload_reachable_as_attributes(self):
        payload = {"location_message": {"latitude": 1.0}, "newField": "value"}
        resolved = resolve(MarkerResponse, payload, parsing_response=True)

        assert isinstance(resolved, SinchRawResponse)
        assert resolved.newField == "value"
        assert resolved.location_message == {"latitude": 1.0}

    def test_unknown_serializes_back_to_the_payload_it_wrapped(self):
        payload = {"location_message": {"latitude": 1.0}}
        resolved = resolve(MarkerResponse, payload, parsing_response=True)

        assert resolved.model_dump() == payload
