import json

from diary.models import Diary


def save(event, context):
    body = json.loads(event['body'])

    diary = Diary()
    page = diary.write(body['note'])

    response = {
        "id": diary.id.id,
        "note": page.note,
        "postedAt": page.posted_at.isoformat()
    }

    return {
        'statusCode': 201,
        'body': json.dumps(response)
    }
