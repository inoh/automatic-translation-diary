import os
import boto3
from diary.models import (Diary, DiaryId, DiaryRepository)


class DynamoDBDiaryRepository(DiaryRepository):

    def diaries(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('DYNAMODB_NAME_PAGES'))
        diaries = []
        for item in table.scan()['Items']:
            diary = Diary()
            diary.id = DiaryId(item['diary_id'])
            diaries.append(diary)
        return diaries
