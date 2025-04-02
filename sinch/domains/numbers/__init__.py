from sinch.domains.numbers.api.v1 import (
    ActiveNumbers, AvailableNumbers, AvailableRegions, Callback
)


class NumbersBase:
    """
    Documentation for Sinch virtual Numbers is found at https://developers.sinch.com/docs/numbers/.
    """
    def __init__(self, sinch):
        self._sinch = sinch


class Numbers(NumbersBase):
    """
    Synchronous version of the Numbers Domain
    """
    __doc__ += NumbersBase.__doc__

    def __init__(self, sinch):
        super(Numbers, self).__init__(sinch)
        self.available = AvailableNumbers(self._sinch)
        self.regions = AvailableRegions(self._sinch)
        self.active = ActiveNumbers(self._sinch)
        self.callback_configuration = Callback(self._sinch)
