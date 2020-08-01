import uuid
from datetime import datetime

from .page_id import PageId
from .lang import Lang
from diary.models import DiaryId


class Page:

    id: PageId
    note: str
    posted_at: datetime


    @classmethod
    def create(cls, diary_id: DiaryId, note: str):
        page = cls()
        page.id = PageId(diary_id, Lang.Ja)
        page.note = note
        page.posted_at = datetime.now()
        return page
