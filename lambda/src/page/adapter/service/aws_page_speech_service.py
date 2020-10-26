import boto3
from contextlib import closing
from page.models import (Page, PageTranslator, PageSpeechService, Lang)


client = boto3.client('polly')


class AWSPageSpeechService(PageSpeechService):

    def speech(self, text: str):
        response = client.synthesize_speech(
            Engine='standard',
            LanguageCode='es-US', # 'ja-JP'
            OutputFormat='mp3', # 'json'|'mp3'|'ogg_vorbis'|'pcm',
            Text=text,
            VoiceId='Joanna' # https://aws.amazon.com/jp/polly/features/
        )

        if "AudioStream" not in response:
            return None

        with closing(response["AudioStream"]) as stream:
            return stream.read()
