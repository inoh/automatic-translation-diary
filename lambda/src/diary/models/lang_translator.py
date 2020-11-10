from abc import ABCMeta, abstractmethod


from diary.models import Lang


class LangTranslator(metaclass=ABCMeta):

    @abstractmethod
    def translate(self, note: str, lang: Lang) -> (str, Lang):
        pass
