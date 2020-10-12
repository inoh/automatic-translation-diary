from abc import ABCMeta, abstractmethod


from page.models import Page


class PageSpeechService(metaclass=ABCMeta):

    @abstractmethod
    def speech(self, text: str):
        pass
