import uuid
from typing import Dict
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

    def __eq__(self, other):
        return self.name == other.name


@dataclass(frozen=True)
class Page:

    note: str
    lang: Lang
    posted_at: datetime

    def __eq__(self, other):
        return self.note == other.note and \
                self.lang == other.lang and \
                self.posted_at == other.posted_at


@dataclass(frozen=True)
class DiaryId:

    raw: str

    def __eq__(self, other):
        return self.raw == other.raw


class Diary:

    id: DiaryId
    title: str
    pages: Dict[Lang, Page]

    @classmethod
    def create(cls, title: str):
        diary = cls()
        diary.id = DiaryId(str(uuid.uuid4()))
        diary.title = title
        diary.pages = {}
        return diary


    def write_page(self, note: str, lang: Lang) -> Page:
        page = Page(
            note, lang, datetime.now()
        )

        self.pages[lang] = page

        return page
