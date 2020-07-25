import uuid

from .diary_id import DiaryId
from page.models import Page


class Diary:
    id: DiaryId

    @classmethod
    def create(cls):
        diary = cls()
        diary.id = DiaryId(str(uuid.uuid4()))
        return diary

    def write(self, note: str):
        return Page(self.id, note)
