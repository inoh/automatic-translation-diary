import json
import base64
from page.page_usecase import PageUsecase
from page.adapter.repository.dynamodb_page_repository import DynamoDBPageRepository
from page.adapter.service.aws_page_translator import AWSPageTranslator
from page.adapter.service.aws_page_speech_service import AWSPageSpeechService


page_usecase = PageUsecase(
    DynamoDBPageRepository(),
    AWSPageTranslator(),
    AWSPageSpeechService()
)


def page(event, context):
    params = event['pathParameters']

    page = page_usecase.page(params['diaryId'], params['lang'])

    response = {
        "id": page.id.diary_id.id,
        "lang": page.id.lang.name,
        "note": page.note,
        "postedAt": page.posted_at.isoformat()
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def translate(event, context):
    for record in event['Records']:
        if record['eventName'] == 'REMOVE':
            # TODO: delete record
            pass
        else:
            page_id = record['dynamodb']['NewImage']['id']['S']
            page_usecase.translate(page_id)


def speech(event, context):
    params = event['pathParameters']

    stream = page_usecase.speech(params['diaryId'], params['lang'])

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename="speech.mp3"'
        },
        'body': base64.b64encode(stream),
        'isBase64Encoded': True
    }
