from abc import ABCMeta, abstractmethod
from typing import List
from diary.models import (Diary, Lang)


class DiaryRepository(metaclass=ABCMeta):

    @abstractmethod
    def save(self, diary: Diary):
        pass

    @abstractmethod
    def diaries(self, lang: Lang) -> List[Diary]:
        pass

    @abstractmethod
    def diary(self) -> Diary:
        pass
