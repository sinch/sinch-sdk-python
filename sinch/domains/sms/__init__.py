from sinch.domains.sms.api.v1.delivery_reports_apis import DeliveryReports

# from sinch.domains.sms.api.v1.groups_apis import Groups
# from sinch.domains.sms.api.v1.inbounds_apis import Inbounds
# from sinch.domains.sms.api.v1.webhooks_apis import Webhooks
from sinch.domains.sms.api.v1.batches_apis import Batches


class SMS:
    def __init__(self, sinch):
        self._sinch = sinch
        self.delivery_reports = DeliveryReports(sinch)
        # self.groups = Groups(sinch)
        # self.inbounds = Inbounds(sinch)
        # self.webhooks = Webhooks(sinch)
        self.batches = Batches(sinch)
