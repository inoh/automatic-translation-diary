import json
from diary.models import DiaryId
from page.models import (PageRepository, PageId, Lang)
from page.adapter.repository.dynamodb_page_repository import DynamoDBPageRepository


page_repository: PageRepository = DynamoDBPageRepository()


def page(event, context):
    params = event['pathParameters']

    diary_id = DiaryId(params['diaryId'])
    page = page_repository.page(PageId(diary_id, Lang.Ja))

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
