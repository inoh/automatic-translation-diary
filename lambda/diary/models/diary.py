import uuid

from .diary_id import DiaryId
from page.models import Page


class Diary:
    id: DiaryId

    def __init__(self):
        self.id = DiaryId(str(uuid.uuid4()))


    def write(self, note: str):
        return Page(self.id, note)
