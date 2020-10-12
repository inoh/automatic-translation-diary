import json
from diary.models import DiaryId
from page.models import (
    Page, PageRepository, PageTranslator, PageSpeechService, PageId, Lang)


class PageUsecase():

    def __init__(self,
            page_repository: PageRepository,
            page_translator: PageTranslator,
            page_speech_service: PageSpeechService):
        self.page_repository = page_repository
        self.page_translator = page_translator
        self.page_speech_service = page_speech_service


    def page(self, diary_id: str, lang: str) -> Page:
        page = self.page_repository.page(self._page_id(diary_id, lang))

        return page


    def translate(self, page_id: str) -> Page:
        diary_id, lang = page_id.split(':')
        page_ja = self.page_repository.page(self._page_id(diary_id, lang))

        page_en = self.page_translator.translate(page_ja, Lang.En)

        self.page_repository.save(page_en)

        return page_en


    def speech(self, diary_id: str, lang: str) -> str:
        page = self.page_repository.page(self._page_id(diary_id, lang))

        return self.page_speech_service.speech(page.note)


    def _page_id(self, diary_id: str, lang: str) -> PageId:
        return PageId(DiaryId(diary_id), Lang.value_of(lang))
