from dataclasses import dataclass

from .lang import Lang
from diary.models import DiaryId


@dataclass(frozen=True)
class PageId:
    diary_id: DiaryId
    lang: Lang

    def __eq__(self, other):
        return (self.diary_id == other.diary_id) and \
               (self.lang == other.lang)
