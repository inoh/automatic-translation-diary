from .models import (
    Diary, DiaryId, Lang, DiaryRepository, LangTranslator, SpeekingService)


class DiaryUsecase():

    def __init__(self,
                 diary_repository: DiaryRepository,
                 lang_translator: LangTranslator,
                 speeking_service: SpeekingService):
        self.diary_repository = diary_repository
        self.lang_translator = lang_translator
        self.speeking_service = speeking_service

    def save(self, title: str, note: str, lang: str):
        diary = Diary.create(title)
        page = diary.write_page(note, Lang.value_of(lang))

        translated = self.lang_translator.translate(page.note, page.lang)

        diary.write_page(*translated)

        self.diary_repository.save(diary)

        return diary

    def diaries(self):
        return self.diary_repository.diaries()

    def speech(self, id: str, lang: str) -> str:
        diary = self.diary_repository.diary(
            DiaryId(id))

        return self.speeking_service.speek(
            diary.pages[Lang.value_of(lang)].note)
