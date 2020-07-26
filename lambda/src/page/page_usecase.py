import json
from diary.models import DiaryId
from page.models import (Page, PageRepository, PageId, Lang)


class PageUsecase():

    def __init__(self, page_repository: PageRepository):
        self.page_repository = page_repository


    def page(self, diary_id: str, lang: str) -> Page:
        diary_id = DiaryId(diary_id)
        page = self.page_repository.page(PageId(diary_id, Lang.value_of(lang)))

        return page
