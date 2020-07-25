from .models import (Diary, DiaryRepository)
from page.models import PageRepository


class DiaryUsecase():

    def __init__(self,
                 diary_repository: DiaryRepository,
                 page_repository: PageRepository):
        self.diary_repository = diary_repository
        self.page_repository = page_repository


    def save(self, note: str) -> Diary:
        diary = Diary.create()
        page = diary.write(note)

        self.page_repository.save(page)

        return diary


    def diaries(self):
        return self.diary_repository.diaries()
