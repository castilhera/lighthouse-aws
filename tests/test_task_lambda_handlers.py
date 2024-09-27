import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'tasks', 'api', 'runtime'))

import boto3
import json
import mock
import unittest
from moto import mock_aws
from tasks.api.runtime import (
    create_task,
    get_task,
    update_task,
    delete_task,
    tasks_db
)

@mock_aws
class TestTaskLambdaHandlers(unittest.TestCase):

    table_name = "TasksTable"

    def setUp(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

        dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {'AttributeName': 'taskId', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'taskId', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        self.enterContext(
            mock.patch.dict(
                os.environ,
                {
                    "TASKS_TABLE": self.table_name
                }
            )
        )

        self.db = tasks_db.TasksDatabase(self.table_name)

    def test_create_task(self):
        event = {
            "body": json.dumps(
                {
                    "title": "Task 1",
                    "description": "This is task 1",
                    "status": "pending"
                }
            )
        }
        context = {}
        response = create_task.handler(event, context)
        self.assertEqual(response["statusCode"], 201)
        self.assertIn("body", response)

    def test_get_task(self):
        task = self.db.create_task("task name", "task description", "pending")

        event = {
            'pathParameters': {
                'taskId': task['taskId']
            }
        }
        context = {}

        response = get_task.handler(event, context)
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("body", response)
        task = json.loads(response["body"])
        self.assertEqual(task['taskId'], task["taskId"])

    def test_update_task(self):
        task = self.db.create_task("task name", "task description", "pending")

        event = {
            'pathParameters': {
                'taskId': task['taskId']
            },
            "body": json.dumps(
                {
                    "title": "Updated Task 1",
                    "description": "This task has been updated",
                    "status": "completed"
                }
            )
        }
        context = {}

        response = update_task.handler(event, context)
        self.assertEqual(response["statusCode"], 204)

    def test_delete_task(self):
        task = self.db.create_task("task name", "task description", "pending")

        event = {
            'pathParameters': {
                'taskId': task['taskId']
            }
        }
        context = {}

        response = delete_task.handler(event, context)
        self.assertEqual(response["statusCode"], 204)

if __name__ == '__main__':
    unittest.main(verbosity=2)
