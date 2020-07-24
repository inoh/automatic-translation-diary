import json
from diary.models import Diary
from page.models import PageRepository
from page.adapter.repository.dynamodb_page_repository import DynamoDBPageRepository


page_repository: PageRepository = DynamoDBPageRepository()

def save(event, context):
    body = json.loads(event['body'])

    diary = Diary()
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
