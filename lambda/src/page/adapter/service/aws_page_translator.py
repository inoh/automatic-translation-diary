import os
import boto3
from page.models import (Page, PageTranslator, Lang)


class AWSPageTranslator(PageTranslator):

    def translate(self, page: Page, target_lang: Lang) -> Page:
        translate = boto3.client(service_name='translate', use_ssl=True)

        result = translate.translate_text(Text=page.note, 
                    SourceLanguageCode=page.id.lang.name,
                    TargetLanguageCode=target_lang.name)

        return Page.create(
            page.id.diary_id,
            target_lang,
            result.get('TranslatedText'))
