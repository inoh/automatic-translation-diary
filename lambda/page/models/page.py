import uuid
from datetime import datetime

from .page_id import PageId
from .lang import Lang
from diary.models import DiaryId


class Page:
    id: PageId
    note: str
    posted_at: datetime

    def __init__(self, diary_id: DiaryId, note: str):
        self.id = PageId(diary_id, Lang.Ja)
        self.note = note
        self.posted_at = datetime.now()
