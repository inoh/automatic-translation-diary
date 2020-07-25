import json
from page.page_usecase import PageUsecase
from page.adapter.repository.dynamodb_page_repository import DynamoDBPageRepository


usecase = PageUsecase(
    DynamoDBPageRepository()
)


def page(event, context):
    params = event['pathParameters']

    page = usecase.page(params['diaryId'], params['lang'])

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
