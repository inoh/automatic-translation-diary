import os
import boto3
from diary.models import (Diary, DiaryId, DiaryRepository)
from boto3.dynamodb.conditions import Key


class DynamoDBDiaryRepository(DiaryRepository):

    def diaries(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('DYNAMODB_NAME_PAGES'))
        diaries = []
        for item in table.scan(
            FilterExpression=Key('lang').eq('Ja')
        )['Items']:
            diary = Diary()
            diary.id = DiaryId(item['diary_id'])
            diaries.append(diary)
        return diaries
