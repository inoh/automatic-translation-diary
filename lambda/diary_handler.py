import json
from diary.diary_usecase import DiaryUsecase
from diary.adapter.repository.dynamodb_diary_repository import DynamoDBDiaryRepository
from page.adapter.repository.dynamodb_page_repository import DynamoDBPageRepository


usecase = DiaryUsecase(
    DynamoDBDiaryRepository(),
    DynamoDBPageRepository()
)


def save(event, context):
    body = json.loads(event['body'])

    diary = usecase.save(body['note'])

    response = {
        "id": diary.id.id
    }

    return {
        'statusCode': 201,
        'body': json.dumps(response)
    }


def diaries(event, context):
    diaries = usecase.diaries()

    response = [{
        "id": diary.id.id
    } for diary in diaries]

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
