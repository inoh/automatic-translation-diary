import json
import base64
from diary.diary_usecase import DiaryUsecase
from diary.adapter.repository.dynamodb_diary_repository import DynamoDBDiaryRepository
from diary.adapter.service.aws_lang_translator import AWSLangTranslator
from diary.adapter.service.aws_speeking_service import AWSSpeekingService


diary_usecase = DiaryUsecase(
    DynamoDBDiaryRepository(),
    AWSLangTranslator(),
    AWSSpeekingService()
)


def save(event, context):
    params = event['pathParameters']
    body = json.loads(event['body'])

    diary = diary_usecase.save(body['title'], body['note'], params['lang'])

    response = _render_diary(diary)

    return {
        'statusCode': 201,
        'body': json.dumps(response)
    }


def diaries(event, context):
    diaries = diary_usecase.diaries()

    response = [_render_diary(diary) for diary in diaries]

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def speech(event, context):
    params = event['pathParameters']

    stream = diary_usecase.speech(params['diaryId'], params['lang'])

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename="speech.mp3"'
        },
        'body': base64.b64encode(stream),
        'isBase64Encoded': True
    }


def _render_diary(diary):
    response = {
        'id': diary.id.raw,
        'title': diary.title,
        'pages': {},
    }

    for page in diary.pages.values():
        response['pages'][page.lang.name] = {
            'note': page.note,
            'posted_at': page.posted_at.isoformat(),
        }

    return response
