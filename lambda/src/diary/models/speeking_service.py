from abc import ABCMeta, abstractmethod


class SpeekingService(metaclass=ABCMeta):

    @abstractmethod
    def speek(self, text: str):
        pass
