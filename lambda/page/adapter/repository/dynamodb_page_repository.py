import boto3
from page.models import (Page, PageRepository)


class DynamoDBPageRepository(PageRepository):
    def save(self, page: Page):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Pages')
        response = table.put_item(
            Item={
                'id': f'{page.id.diary_id.id}:{page.id.lang.name}',
                'diary_id': page.id.diary_id.id,
                'lang': page.id.lang.name,
                'note': page.note,
                'posted_at': int(page.posted_at.timestamp())
            }
        )
