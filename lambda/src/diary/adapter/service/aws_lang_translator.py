import os
import boto3
from diary.models import (Diary, LangTranslator, Lang)


class AWSLangTranslator(LangTranslator):

    def translate(self, note: str, lang: Lang) -> (str, Lang):
        translate = boto3.client(service_name='translate', use_ssl=True)

        target = Lang.En if lang == Lang.Ja else Lang.Ja

        result = translate.translate_text(Text=note, 
                                          SourceLanguageCode=lang.name,
                                          TargetLanguageCode=target.name)

        return (result.get('TranslatedText'), target)
