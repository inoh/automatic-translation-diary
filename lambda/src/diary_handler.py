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

    diary, trans_diary = diary_usecase.save(body['note'], params['lang'])

    ja_diary, en_diary = (diary, trans_diary) if params['lang'] == 'Ja' else (trans_diary, diary)

    response = {
        'id': diary.id.id,
        'posted_at': diary.posted_at.isoformat(),
        'Ja': {
            'note': ja_diary.note
        },
        'En': {
            'note': en_diary.note
        }
    }

    return {
        'statusCode': 201,
        'body': json.dumps(response)
    }


def diaries(event, context):
    params = event['pathParameters']

    diaries = diary_usecase.diaries(params['lang'])

    response = [{
        'id': diary.id.id,
        'posted_at': diary.posted_at.isoformat(),
        diary.id.lang.name: {
            'note': diary.note
        }
    } for diary in diaries]

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
