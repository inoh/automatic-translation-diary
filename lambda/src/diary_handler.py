import json
from diary.diary_usecase import DiaryUsecase
from diary.adapter.repository.dynamodb_diary_repository import DynamoDBDiaryRepository
from page.page_usecase import PageUsecase
from page.adapter.repository.dynamodb_page_repository import DynamoDBPageRepository
from page.adapter.service.aws_page_translator import AWSPageTranslator
from page.adapter.service.aws_page_speech_service import AWSPageSpeechService


page_repository = DynamoDBPageRepository()
diary_usecase = DiaryUsecase(
    DynamoDBDiaryRepository(),
    page_repository
)
page_usecase = PageUsecase(
    page_repository,
    AWSPageTranslator(),
    AWSPageSpeechService()
)


def save(event, context):
    body = json.loads(event['body'])

    diary = diary_usecase.save(body['note'])
    page_usecase.translate(
        f'{diary.id.id}:Ja')

    response = {
        "id": diary.id.id
    }

    return {
        'statusCode': 201,
        'body': json.dumps(response)
    }


def diaries(event, context):
    diaries = diary_usecase.diaries()

    response = [{
        "id": diary.id.id
    } for diary in diaries]

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
