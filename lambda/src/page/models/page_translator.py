from abc import ABCMeta, abstractmethod


from page.models import Page


class PageTranslator(metaclass=ABCMeta):

    @abstractmethod
    def translate(self, page: Page):
        pass
