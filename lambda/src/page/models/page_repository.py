from abc import ABCMeta, abstractmethod
from .page import Page
from .page_id import PageId


class PageRepository(metaclass=ABCMeta):

    @abstractmethod
    def save(self, page: Page):
        pass


    @abstractmethod
    def page(self, page_id: PageId) -> Page:
        pass
