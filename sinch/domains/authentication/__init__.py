from abc import ABC, abstractmethod


class AuthenticationBase(ABC):
    def __init__(self, sinch):
        self.sinch = sinch

    @abstractmethod
    def get_auth_token(self):
        pass

    @abstractmethod
    def set_auth_token(self, token):
        pass


class Authentication(AuthenticationBase):
    def get_auth_token(self):
        return self.sinch.configuration.token_manager.get_auth_token()

    def set_auth_token(self, token):
        self.sinch.configuration.token_manager.set_auth_token(token)
