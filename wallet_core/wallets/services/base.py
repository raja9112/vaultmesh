from abc import ABC, abstractmethod


class BaseWalletService(ABC):

    @abstractmethod
    def create_wallet(self):
        pass