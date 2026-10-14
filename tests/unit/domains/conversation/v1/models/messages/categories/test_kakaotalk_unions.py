import pytest
from pydantic import TypeAdapter, ValidationError

from sinch.core.models.internal.unions import response_parsing_scope
from sinch.core.models.sinch_raw_response import SinchRawResponse
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons.kakaotalk_app_link_button import (  # noqa: E501
    KakaoTalkAppLinkButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons.kakaotalk_bot_keyword_button import (  # noqa: E501
    KakaoTalkBotKeywordButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.buttons.kakaotalk_web_link_button import (  # noqa: E501
    KakaoTalkWebLinkButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_discount_fixed_commerce import (  # noqa: E501
    KakaoTalkDiscountFixedCommerce,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_discount_rate_commerce import (  # noqa: E501
    KakaoTalkDiscountRateCommerce,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_regular_price_commerce import (  # noqa: E501
    KakaoTalkRegularPriceCommerce,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.coupons.kakaotalk_discount_rate_coupon import (  # noqa: E501
    KakaoTalkDiscountRateCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.coupons.kakaotalk_fixed_discount_coupon import (  # noqa: E501
    KakaoTalkFixedDiscountCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.coupons.kakaotalk_free_coupon import (  # noqa: E501
    KakaoTalkFreeCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.coupons.kakaotalk_shipping_discount_coupon import (  # noqa: E501
    KakaoTalkShippingDiscountCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.coupons.kakaotalk_up_coupon import (  # noqa: E501
    KakaoTalkUpCoupon,
)
from sinch.domains.conversation.models.v1.messages.response.types.kakaotalk_button import (  # noqa: E501
    KakaoTalkButton,
)
from sinch.domains.conversation.models.v1.messages.response.types.kakaotalk_commerce import (  # noqa: E501
    KakaoTalkCommerce,
)
from sinch.domains.conversation.models.v1.messages.response.types.kakaotalk_coupon import (  # noqa: E501
    KakaoTalkCoupon,
)

button_adapter = TypeAdapter(KakaoTalkButton)
commerce_adapter = TypeAdapter(KakaoTalkCommerce)
coupon_adapter = TypeAdapter(KakaoTalkCoupon)


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        (
            {"name": "Shop", "link_mo": "https://m.example.com"},
            KakaoTalkWebLinkButton,
        ),
        (
            {
                "name": "Open app",
                "scheme_ios": "example://shop",
                "scheme_android": "example://shop",
            },
            KakaoTalkAppLinkButton,
        ),
        ({"name": "Help"}, KakaoTalkBotKeywordButton),
    ],
    ids=["web_link", "app_link", "bot_keyword"],
)
def test_kakaotalk_button_resolves_each_variant(payload, expected_type):
    """
    Expects each button variant to resolve from the fields it declares.
    """
    assert type(button_adapter.validate_python(payload)) is expected_type


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        (
            {"title": "A product", "regular_price": 1000},
            KakaoTalkRegularPriceCommerce,
        ),
        (
            {
                "title": "A product",
                "regular_price": 1000,
                "discount_price": 800,
                "discount_fixed": 200,
            },
            KakaoTalkDiscountFixedCommerce,
        ),
        (
            {
                "title": "A product",
                "regular_price": 1000,
                "discount_price": 800,
                "discount_rate": 20,
            },
            KakaoTalkDiscountRateCommerce,
        ),
    ],
    ids=["regular_price", "discount_fixed", "discount_rate"],
)
def test_kakaotalk_commerce_resolves_each_variant(payload, expected_type):
    """
    Expects each commerce variant to resolve from its own discount fields.
    """
    assert type(commerce_adapter.validate_python(payload)) is expected_type


@pytest.mark.parametrize(
    "payload, expected_type",
    [
        (
            {"type": "FIXED_DISCOUNT_COUPON", "discount_fixed": 500},
            KakaoTalkFixedDiscountCoupon,
        ),
        (
            {"type": "PERCENTAGE_DISCOUNT_COUPON", "discount_rate": 10},
            KakaoTalkDiscountRateCoupon,
        ),
        (
            {"type": "SHIPPING_DISCOUNT_COUPON"},
            KakaoTalkShippingDiscountCoupon,
        ),
        ({"type": "FREE_COUPON", "title": "A gift"}, KakaoTalkFreeCoupon),
        ({"type": "UP_COUPON", "title": "Up to"}, KakaoTalkUpCoupon),
    ],
    ids=["fixed", "rate", "shipping", "free", "up"],
)
def test_kakaotalk_coupon_resolves_each_variant(payload, expected_type):
    """
    Expects each coupon variant to resolve from its type field.
    """
    assert type(coupon_adapter.validate_python(payload)) is expected_type


def test_kakaotalk_coupon_resolves_an_unknown_type_to_unknown_in_a_response():
    """
    Expects a coupon type added to the API later to be parsed as SinchRawResponse
    instead of failing the whole message.
    """
    payload = {"type": "SOMETHING_NEW", "title": "A coupon"}

    with response_parsing_scope():
        coupon = coupon_adapter.validate_python(payload)

    assert isinstance(coupon, SinchRawResponse)
    assert coupon.model_dump() == payload


def test_kakaotalk_coupon_rejects_an_unknown_type_in_a_request():
    """
    Expects the same coupon type to be rejected when the caller is building a
    message rather than parsing one.
    """
    with pytest.raises(ValidationError, match="does not match any of the expected tags"):
        coupon_adapter.validate_python({"type": "SOMETHING_NEW"})
