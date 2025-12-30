from sinch.domains.conversation.models.v1.messages.response.shared.choice_response_message import (
    ChoiceResponseMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.fallback_message import (
    FallbackMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.media_card_message import (
    MediaCardMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.product_response_message import (
    ProductResponseMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.template_message import (
    TemplateMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.text_message import (
    TextMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.url_message import (
    UrlMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.calendar_message import (
    CalendarMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.call_message import (
    CallMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.share_location_message import (
    ShareLocationMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.message_properties import (
    MessageProperties,
)
from sinch.domains.conversation.models.v1.messages.response.shared.list_message_properties import (
    ListMessageProperties,
)
from sinch.domains.conversation.models.v1.messages.response.shared.template_reference import (
    TemplateReference,
)
from sinch.domains.conversation.models.v1.messages.response.shared.template_reference_with_version import (
    TemplateReferenceWithVersion,
)
from sinch.domains.conversation.models.v1.messages.response.shared.list_item_choice import (
    ListItemChoice,
)
from sinch.domains.conversation.models.v1.messages.response.shared.list_item_product import (
    ListItemProduct,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_body import (
    WhatsAppInteractiveBody,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_footer import (
    WhatsAppInteractiveFooter,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_header_media import (
    WhatsAppInteractiveHeaderMedia,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_text_header import (
    WhatsAppInteractiveTextHeader,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_image_header import (
    WhatsAppInteractiveImageHeader,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_document_header import (
    WhatsAppInteractiveDocumentHeader,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_video_header import (
    WhatsAppInteractiveVideoHeader,
)
from sinch.domains.conversation.models.v1.messages.response.shared.channel_specific_message import (
    ChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.channel_specific_contact_message_message import (
    ChannelSpecificContactMessageMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.choice_options import (
    CallChoiceMessage,
    CalendarChoiceMessage,
    ChoiceMessageWithPostback,
    LocationChoiceMessage,
    ShareLocationChoiceMessage,
    TextChoiceMessage,
    UrlChoiceMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.app_message import (
    CardAppMessage,
    CarouselAppMessage,
    ChoiceAppMessage,
    ContactInfoAppMessage,
    ListAppMessage,
    LocationAppMessage,
    MediaAppMessage,
    TemplateAppMessage,
    TextAppMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.contact_message import (
    ChannelSpecificContactMessage,
    ChoiceResponseContactMessage,
    FallbackContactMessage,
    LocationContactMessage,
    MediaCardContactMessage,
    MediaContactMessage,
    ProductResponseContactMessage,
    TextContactMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.dynamic_pix import (
    DynamicPix,
)
from sinch.domains.conversation.models.v1.messages.response.shared.payment_link import (
    PaymentLink,
)
from sinch.domains.conversation.models.v1.messages.response.shared.boleto import (
    Boleto,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_payment_settings_pix import (
    WhatsAppPaymentSettingsPix,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_payment_settings_payment_link import (
    WhatsAppPaymentSettingsPaymentLink,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_payment_settings_boleto import (
    WhatsAppPaymentSettingsBoleto,
)
from sinch.domains.conversation.models.v1.messages.response.shared.order_item import (
    OrderItem,
)
from sinch.domains.conversation.models.v1.messages.response.shared.payment_order import (
    PaymentOrder,
)
from sinch.domains.conversation.models.v1.messages.response.shared.payment_order_status_order import (
    PaymentOrderStatusOrder,
)
from sinch.domains.conversation.models.v1.messages.response.shared.payment_order_status_content import (
    PaymentOrderStatusContent,
)
from sinch.domains.conversation.models.v1.messages.response.shared.payment_order_details_content import (
    PaymentOrderDetailsContent,
)
from sinch.domains.conversation.models.v1.messages.response.shared.flow_action_payload import (
    FlowActionPayload,
)
from sinch.domains.conversation.models.v1.messages.response.shared.flow_channel_specific_message import (
    FlowChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.payment_order_details_channel_specific_message import (
    PaymentOrderDetailsChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.payment_order_status_channel_specific_message import (
    PaymentOrderStatusChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_channel_specific_message import (
    KakaoTalkChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_commerce_image import (
    KakaoTalkCommerceImage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_carousel_head import (
    KakaoTalkCarouselHead,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_carousel_tail import (
    KakaoTalkCarouselTail,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_commerce_message import (
    KakaoTalkCommerceMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_carousel import (
    KakaoTalkCarousel,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_commerce_channel_specific_message import (
    KakaoTalkCommerceChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_carousel_commerce_channel_specific_message import (
    KakaoTalkCarouselCommerceChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_button import (
    KakaoTalkButton,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_web_link_button import (
    KakaoTalkWebLinkButton,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_app_link_button import (
    KakaoTalkAppLinkButton,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_bot_keyword_button import (
    KakaoTalkBotKeywordButton,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_coupon import (
    KakaoTalkCoupon,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_regular_price_commerce import (
    KakaoTalkRegularPriceCommerce,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_discount_fixed_commerce import (
    KakaoTalkDiscountFixedCommerce,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_discount_rate_commerce import (
    KakaoTalkDiscountRateCommerce,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_fixed_discount_coupon import (
    KakaoTalkFixedDiscountCoupon,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_discount_rate_coupon import (
    KakaoTalkDiscountRateCoupon,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_shipping_discount_coupon import (
    KakaoTalkShippingDiscountCoupon,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_free_coupon import (
    KakaoTalkFreeCoupon,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_up_coupon import (
    KakaoTalkUpCoupon,
)
from sinch.domains.conversation.models.v1.messages.response.shared.reply_to import (
    ReplyTo,
)
from sinch.domains.conversation.models.v1.messages.response.shared.omni_message_override import (
    OmniMessageOverride,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_interactive_nfm_reply import (
    WhatsAppInteractiveNfmReply,
)

__all__ = [
    "CalendarMessage",
    "CallMessage",
    "CardMessage",
    "CarouselMessage",
    "ChannelSpecificMessage",
    "ChoiceMessage",
    "ChoiceResponseMessage",
    "ContactInfoMessage",
    "FallbackMessage",
    "ListMessage",
    "ListItemChoice",
    "ListItemProduct",
    "ListMessageProperties",
    "LocationMessage",
    "MediaCardMessage",
    "MediaProperties",
    "MessageProperties",
    "ProductResponseMessage",
    "ShareLocationMessage",
    "TemplateMessage",
    "TemplateReference",
    "TemplateReferenceWithVersion",
    "TextMessage",
    "UrlMessage",
    "ChannelSpecificContactMessageMessage",
    "CallChoiceMessage",
    "CalendarChoiceMessage",
    "ChoiceMessageWithPostback",
    "LocationChoiceMessage",
    "ShareLocationChoiceMessage",
    "TextChoiceMessage",
    "UrlChoiceMessage",
    "WhatsAppInteractiveBody",
    "WhatsAppInteractiveDocumentHeader",
    "WhatsAppInteractiveFooter",
    "WhatsAppInteractiveHeaderMedia",
    "WhatsAppInteractiveImageHeader",
    "WhatsAppInteractiveTextHeader",
    "WhatsAppInteractiveVideoHeader",
    "AppMessage",
    "CardAppMessage",
    "CarouselAppMessage",
    "ChoiceAppMessage",
    "ContactInfoAppMessage",
    "ListAppMessage",
    "LocationAppMessage",
    "MediaAppMessage",
    "TemplateAppMessage",
    "TextAppMessage",
    "ContactMessage",
    "ChannelSpecificContactMessage",
    "ChoiceResponseContactMessage",
    "FallbackContactMessage",
    "LocationContactMessage",
    "MediaCardContactMessage",
    "MediaContactMessage",
    "ProductResponseContactMessage",
    "TextContactMessage",
    "DynamicPix",
    "PaymentLink",
    "Boleto",
    "WhatsAppPaymentSettingsPix",
    "WhatsAppPaymentSettingsPaymentLink",
    "WhatsAppPaymentSettingsBoleto",
    "OrderItem",
    "PaymentOrder",
    "PaymentOrderStatusOrder",
    "PaymentOrderStatusContent",
    "PaymentOrderDetailsContent",
    "FlowActionPayload",
    "FlowChannelSpecificMessage",
    "PaymentOrderDetailsChannelSpecificMessage",
    "PaymentOrderStatusChannelSpecificMessage",
    "KakaoTalkChannelSpecificMessage",
    "KakaoTalkCommerceImage",
    "KakaoTalkCarouselHead",
    "KakaoTalkCarouselTail",
    "KakaoTalkCommerceMessage",
    "KakaoTalkCarousel",
    "KakaoTalkCommerceChannelSpecificMessage",
    "KakaoTalkCarouselCommerceChannelSpecificMessage",
    "KakaoTalkButton",
    "KakaoTalkWebLinkButton",
    "KakaoTalkAppLinkButton",
    "KakaoTalkBotKeywordButton",
    "KakaoTalkCoupon",
    "KakaoTalkRegularPriceCommerce",
    "KakaoTalkDiscountFixedCommerce",
    "KakaoTalkDiscountRateCommerce",
    "KakaoTalkFixedDiscountCoupon",
    "KakaoTalkDiscountRateCoupon",
    "KakaoTalkShippingDiscountCoupon",
    "KakaoTalkFreeCoupon",
    "KakaoTalkUpCoupon",
    "ReplyTo",
    "OmniMessageOverride",
    "WhatsAppInteractiveNfmReply",
]


def __getattr__(name: str):
    # Lazy imports to break circular dependencies with fields/
    if name == "CardMessage":
        from sinch.domains.conversation.models.v1.messages.response.shared.card_message import (
            CardMessage,
        )

        return CardMessage
    if name == "CarouselMessage":
        from sinch.domains.conversation.models.v1.messages.response.shared.carousel_message import (
            CarouselMessage,
        )

        return CarouselMessage
    if name == "ChoiceMessage":
        from sinch.domains.conversation.models.v1.messages.response.shared.choice_message import (
            ChoiceMessage,
        )

        return ChoiceMessage
    if name == "ContactInfoMessage":
        from sinch.domains.conversation.models.v1.messages.response.shared.contact_info_message import (
            ContactInfoMessage,
        )

        return ContactInfoMessage
    if name == "ListMessage":
        from sinch.domains.conversation.models.v1.messages.response.shared.list_message import (
            ListMessage,
        )

        return ListMessage
    if name == "LocationMessage":
        from sinch.domains.conversation.models.v1.messages.response.shared.location_message import (
            LocationMessage,
        )

        return LocationMessage
    if name == "MediaProperties":
        from sinch.domains.conversation.models.v1.messages.response.shared.media_properties import (
            MediaProperties,
        )

        return MediaProperties
    if name == "TextMessage":
        from sinch.domains.conversation.models.v1.messages.response.shared.text_message import (
            TextMessage,
        )

        return TextMessage
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
