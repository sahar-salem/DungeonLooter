import time
from abc import ABCMeta, abstractmethod
from typing import Optional


class Token:
    def __init__(self, token: str, expires_in: float) -> None:
        self.token = token
        self._expires_in = expires_in

    @property
    def expired(self) -> bool:
        return time.time() > self._expires_in


class IAuthenticator(metaclass=ABCMeta):
    @abstractmethod
    def login(self) -> Token: ...
