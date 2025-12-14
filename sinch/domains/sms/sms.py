from sinch.domains.sms.api.v1 import (
    Batches,
    DeliveryReports,
)
from sinch.domains.sms.webhooks.v1.sms_webhooks import SmsWebhooks


class SMS:
    """
    Documentation for Sinch SMS is found at
    https://developers.sinch.com/docs/sms/.
    """

    def __init__(self, sinch):
        self._sinch = sinch

        self.batches = Batches(self._sinch)
        self.delivery_reports = DeliveryReports(self._sinch)

    def webhooks(self, callback_secret: str) -> SmsWebhooks:
        """
        Create an SMS webhooks handler with the specified callback secret.

        :param callback_secret: Secret used for webhook validation.
        :type callback_secret: str
        :returns: A configured webhooks handler
        :rtype: SmsWebhooks
        """
        return SmsWebhooks(callback_secret)
