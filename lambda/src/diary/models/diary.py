import uuid
from dataclasses import dataclass
from enum import (Enum, auto)
from datetime import datetime


@dataclass(frozen=True)
class Lang(Enum):

    Ja = auto()
    En = auto()

    @classmethod
    def value_of(cls, name):
        return [lang for lang in cls if lang.name == name][0]


@dataclass(frozen=True)
class DiaryId:

    id: str
    lang: Lang

    def __eq__(self, other):
        return self.id == other.id and \
                self.lang == other.lang


class Diary:

    id: DiaryId
    note: str
    posted_at: datetime

    @classmethod
    def create(cls, id: DiaryId, note: str):
        diary = cls()
        diary.id = id
        diary.note = note
        diary.posted_at = datetime.now()
        return diary
