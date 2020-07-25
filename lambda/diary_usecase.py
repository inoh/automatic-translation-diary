import json
from diary.models import (Diary, DiaryRepository)
from diary.adapter.repository.dynamodb_diary_repository import DynamoDBDiaryRepository
from page.models import PageRepository
from page.adapter.repository.dynamodb_page_repository import DynamoDBPageRepository


diary_repository: DiaryRepository = DynamoDBDiaryRepository()
page_repository: PageRepository = DynamoDBPageRepository()

def save(event, context):
    body = json.loads(event['body'])

    diary = Diary.create()
    page = diary.write(body['note'])

    page_repository.save(page)

    response = {
        "id": diary.id.id,
        "lang": page.id.lang.name,
        "note": page.note,
        "postedAt": page.posted_at.isoformat()
    }

    return {
        'statusCode': 201,
        'body': json.dumps(response)
    }

def diaries(event, context):
    diaries = diary_repository.diaries()

    response = [{"id": diary.id.id} for diary in diaries]

    return {
        'statusCode': 201,
        'body': json.dumps(response)
    }
