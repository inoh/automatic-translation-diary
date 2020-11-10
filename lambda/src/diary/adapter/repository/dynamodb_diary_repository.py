import os
import boto3
from datetime import datetime
from diary.models import (Diary, DiaryId, DiaryRepository, Lang)
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
diaries_table = dynamodb.Table(os.environ.get('DYNAMODB_NAME_DIARIES'))


class DynamoDBDiaryRepository(DiaryRepository):

    def save(self, diary: Diary):
        response = diaries_table.put_item(
            Item={
                'id': f'{diary.id.id}:{diary.id.lang.name}',
                'diary_id': diary.id.id,
                'lang': diary.id.lang.name,
                'note': diary.note,
                'posted_at': int(diary.posted_at.timestamp())
            }
        )

    def diaries(self, lang: Lang):
        diaries = []
        for item in diaries_table.scan(
            FilterExpression=Key('lang').eq(lang.name)
        )['Items']:
            diaries.append(self.__to_diary(item))

        return diaries

    def diary(self, diary_id: DiaryId) -> Diary:
        item = diaries_table.get_item(
            Key={'id': f'{diary_id.id}:{diary_id.lang.name}'})['Item']

        return self.__to_diary(item)

    def __to_diary(self, item) -> Diary:
        diary = Diary()
        diary.id = DiaryId(item['diary_id'], Lang.value_of(item['lang']))
        diary.note = item['note']
        diary.posted_at = datetime.utcfromtimestamp(item['posted_at'])
        return diary
