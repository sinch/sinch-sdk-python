from sinch.domains.sms.api.v1 import (
    Batches,
    DeliveryReports,
)
from sinch.domains.sms.sinch_events.v1.sms_sinch_event import SmsSinchEvent


class SMS:
    """
    Documentation for Sinch SMS is found at
    https://developers.sinch.com/docs/sms/.
    """

    def __init__(self, sinch):
        self._sinch = sinch

        self.batches = Batches(self._sinch)
        self.delivery_reports = DeliveryReports(self._sinch)

    def sinch_events(self, callback_secret: str) -> SmsSinchEvent:
        """
        Create an SMS Sinch Events handler with the specified callback secret.

        :param callback_secret: Secret used for webhook validation.
        :type callback_secret: str
        :returns: A configured Sinch Events handler
        :rtype: SmsSinchEvent
        """
        return SmsSinchEvent(callback_secret)
