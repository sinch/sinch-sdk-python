from sinch.domains.sms.api.v1 import (
    Batches,
    DeliveryReports,
)


class SMS:
    """
    Documentation for Sinch SMS is found at
    https://developers.sinch.com/docs/sms/.
    """

    def __init__(self, sinch):
        self._sinch = sinch

        self.batches = Batches(self._sinch)
        self.delivery_reports = DeliveryReports(self._sinch)
