import uuid
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

    def save(self, note: str, lang: str):
        id = str(uuid.uuid4())

        diary = Diary.create(DiaryId(id, Lang.value_of(lang)), note)
        self.diary_repository.save(diary)

        trans_note, trans_lang = self.lang_translator.translate(
            diary.note, diary.id.lang)

        trans_diary = Diary.create(DiaryId(id, trans_lang), trans_note)
        self.diary_repository.save(trans_diary)

        return (diary, trans_diary)

    def diaries(self, lang: str):
        return self.diary_repository.diaries(Lang.value_of(lang))

    def speech(self, diary_id: str, lang: str) -> str:
        diary = self.diary_repository.diary(
            DiaryId(diary_id, Lang.value_of(lang)))

        return self.speeking_service.speek(diary.note)
