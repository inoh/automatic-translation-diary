from abc import ABCMeta, abstractmethod
from .page import Page


class PageRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, page: Page):
        pass
