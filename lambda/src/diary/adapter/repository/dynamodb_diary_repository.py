import os
import boto3
import json
from datetime import datetime
from diary.models import (Diary, DiaryId, DiaryRepository, Lang, Page)
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
diaries_table = dynamodb.Table(os.environ.get('DYNAMODB_NAME_DIARIES'))


class DynamoDBDiaryRepository(DiaryRepository):

    def save(self, diary: Diary):
        pages = {}
        for page in diary.pages.values():
            pages[page.lang.name] = {
                'note': page.note,
                'posted_at': int(page.posted_at.timestamp()),
            }

        response = diaries_table.put_item(
            Item={
                'id': diary.id.raw,
                'title': diary.title,
                'pages': json.dumps(pages),
            }
        )


    def diaries(self):
        diaries = []
        for item in diaries_table.scan()['Items']:
            diaries.append(self.__to_diary(item))

        return diaries


    def diary(self, diary_id: DiaryId) -> Diary:
        item = diaries_table.get_item(
            Key={'id': diary_id.raw})['Item']

        return self.__to_diary(item)


    def __to_diary(self, item) -> Diary:
        diary = Diary()
        diary.id = DiaryId(item['id'])
        diary.title = item['title']
        diary.pages = {}
        for lang, page in json.loads(item['pages']).items():
            diary.pages[Lang.value_of(lang)] = Page(
                page['note'],
                Lang.value_of(lang),
                datetime.utcfromtimestamp(page['posted_at']),
            )
        return diary
