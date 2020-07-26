import os
import boto3
from datetime import datetime
from page.models import (Page, PageId, PageRepository)


dynamodb = boto3.resource('dynamodb')
pages_table = dynamodb.Table(os.environ.get('DYNAMODB_NAME_PAGES'))


class DynamoDBPageRepository(PageRepository):

    def save(self, page: Page):
        response = pages_table.put_item(
            Item={
                'id': f'{page.id.diary_id.id}:{page.id.lang.name}',
                'diary_id': page.id.diary_id.id,
                'lang': page.id.lang.name,
                'note': page.note,
                'posted_at': int(page.posted_at.timestamp())
            }
        )


    def page(self, page_id: PageId) -> Page:
        item = pages_table.get_item(
            Key={'id': f'{page_id.diary_id.id}:{page_id.lang.name}'})['Item']

        page = Page()
        page.id = page_id
        page.note = item['note']
        page.posted_at = datetime.utcfromtimestamp(item['posted_at'])

        return page
